#!/usr/bin/env python3
"""
Fetch available models from LM Studio and write models.json,
sorted via multi-pass known/unknown parameter classification,
file size mapping heuristics, and descending name tie-breakers.

get_models.py
version 0.5.1
"""

import json
import os
import re
import requests
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================
CONFIG_PATH = "config.json"
OUTPUT_PATH = "models.json"

# ==========================================
# SORTING CONFIGURATION
# ==========================================
REVERSE_PARAMS = False     # Smallest params first (e.g., 230M, 4B, 8B, 24B)
REVERSE_NAME = False       # Descending name tie breaker (Z -> A / apple, banana order)
REVERSE_SIZE = False       # Smallest file size catch-all


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Missing {CONFIG_PATH}. Create it with base_url and optional api_token.")
        raise SystemExit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_headers(token):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def bytes_to_gb(size_bytes):
    if not size_bytes:
        return 0.0
    return round(size_bytes / (1024 ** 3), 2)

def getModelNameParam(name_str):
    """
    Crafty helper to extract parameters from model text (e.g., '24b' from 'lfm2.5-24b-a2b').
    Avoids false positives like 'a2b' by looking for boundary conditions or a preceding dash/dot/space 
    followed by digits and 'b'/'m', but ensuring it isn't part of an internal block like 'a2b'.
    """
    if not name_str or not isinstance(name_str, str):
        return None
    
    cleaned = name_str.lower()
    
    # Search for patterns like '-24b-', '_24b_', or ending with '24b' while ignoring 'a2b' style mid-strings
    matches = re.findall(r'(?:^|[-_./])(\d+(?:\.\d+)?)([bm])(?:$|[-_./])', cleaned)
    if matches:
        val_str, unit = matches[-1] # Take the last matching context if multiple exist
        val = float(val_str)
        if unit == 'm':
            return val / 1000.0
        return val

    # Fallback broader search if strict separators aren't met, checking word boundaries for digits + 'b'
    word_matches = re.findall(r'\b(\d+(?:\.\d+)?)(b)\b', cleaned)
    if word_matches:
        val = float(word_matches[-1][0])
        return val

    return None

def parse_params_to_billions(params_str):
    """
    Safely converts standard parameter strings (e.g., '7B', '230M') into a float value in billions.
    Returns None if the format is complex/unknown (like MoE '32x959M').
    """
    if not params_str or not isinstance(params_str, str):
        return None
    
    p_str = params_str.strip().lower()

    # If it contains 'x', it's an obscure MoE format -> treat as unknown for the strict parameter parser
    if 'x' in p_str:
        return None

    std_match = re.search(r"^([\d.]+)\s*(b|m)?$", p_str)
    if std_match:
        val = float(std_match.group(1))
        unit = std_match.group(2)
        if unit == 'm':
            return val / 1000.0
        return val

    return None

def estimate_param_from_peers(unknown_model, known_models):
    """
    Estimates an unknown model's parameter size based on file size proximity to known models.
    """
    unknown_size = unknown_model.get("size_gb", 0.0)
    if not known_models:
        return 1.0 # Ultimate fallback

    # Find the closest known model by file size delta
    closest = min(known_models, key=lambda k: abs(k["size_gb"] - unknown_size))
    return closest["param_resolved"]

def classify_and_enhance_models(raw_models):
    """
    Processes raw models into enhanced dictionaries containing resolution tags,
    known/unknown categorization, and fallback parameter estimates.
    """
    processed = []
    known_pool = []

    # First pass: Parse knowns and attach raw attributes
    for m in raw_models:
        params_str = m.get("params")
        parsed_val = parse_params_to_billions(params_str)
        
        is_known = parsed_val is not None
        
        item = {
            **m,
            "param_resolved": parsed_val if is_known else 0.0,
            "is_known": is_known,
            "paramEstimate": None
        }
        processed.append(item)
        if is_known:
            known_pool.append(item)

    # Second pass: Resolve unknowns using name extraction or file-size proximity heuristics
    for item in processed:
        if item["is_known"]:
            continue
        
        # Try crafty name extraction first
        name_candidate = getModelNameParam(item.get("key")) or getModelNameParam(item.get("display_name"))
        
        if name_candidate:
            item["paramEstimate"] = name_candidate
            item["param_resolved"] = name_candidate
        else:
            # Fallback to file-size peer approximation against known models
            item["paramEstimate"] = estimate_param_from_peers(item, known_pool)
            item["param_resolved"] = item["paramEstimate"]

    return processed

def main():
    config = load_config()
    base_url = config.get("base_url", "http://localhost:1234").rstrip("/")
    token = config.get("api_token", "")

    url = f"{base_url}/api/v1/models"
    print(f"Fetching models from {url} ...")

    try:
        resp = requests.get(url, headers=get_headers(token), timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch models: {e}")
        raise SystemExit(1)

    data = resp.json()
    raw_models = []
    for m in data.get("models", []):
        if m.get("type") != "llm":
            continue
        quant = m.get("quantization") or {}
        raw_models.append({
            "key": m.get("key"),
            "display_name": m.get("display_name"),
            "params": m.get("params_string"),
            "quant": quant.get("name"),
            "bits_per_weight": quant.get("bits_per_weight"),
            "size_gb": bytes_to_gb(m.get("size_bytes")),
            "architecture": m.get("architecture"),
            "format": m.get("format"),
            "max_context_length": m.get("max_context_length")
        })

    # Step 1: Classify and resolve parameters for known and unknown models
    enhanced_models = classify_and_enhance_models(raw_models)

    # Step 2: Multi-pass stable sorting implementation
    # Priority 3: File size catch-all fallback
    enhanced_models.sort(
        key=lambda x: x["size_gb"] if x["size_gb"] is not None else 0.0,
        reverse=REVERSE_SIZE
    )

    # Priority 2: Model name tie-breaker (Descending: Z -> A)
    enhanced_models.sort(
        key=lambda x: str(x.get("display_name") or x.get("key") or "").lower(),
        reverse=REVERSE_NAME
    )

    # Priority 1: Primary parameter scale (Ascending: smallest models first)
    enhanced_models.sort(
        key=lambda x: x["param_resolved"],
        reverse=REVERSE_PARAMS
    )

    # Clean up internal sorting metadata fields before writing out the final clean file
    output_clean = []
    for m in enhanced_models:
        clean_item = {k: v for k, v in m.items() if k not in ["is_known", "param_resolved"]}
        output_clean.append(clean_item)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output_clean, f, indent=2)

    print(f"Wrote {len(output_clean)} intelligently sorted models to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()