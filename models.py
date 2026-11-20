#!/usr/bin/env python3
"""
Fetch available models from LM Studio and write scenarios/models.json,
sorted by parameter size, name, then file size.

models.py
version 0.6.0
"""

import re
import requests
from pathlib import Path

import config
import utils


def bytes_to_gb(size_bytes):
    if not size_bytes:
        return 0.0
    return round(size_bytes / (1024 ** 3), 2)


def get_model_name_param(name_str):
    if not name_str or not isinstance(name_str, str):
        return None
    cleaned = name_str.lower()
    matches = re.findall(r'(?:^|[-_./])(\d+(?:\.\d+)?)([bm])(?:$|[-_./])', cleaned)
    if matches:
        val_str, unit = matches[-1]
        val = float(val_str)
        if unit == 'm':
            return val / 1000.0
        return val
    # Gemma-style names write the size as e4b / e2b, with no separator before the digits.
    effective = re.findall(r'(?:^|[-_./])e(\d+(?:\.\d+)?)b(?:$|[-_./])', cleaned)
    if effective:
        return float(effective[-1])
    word_matches = re.findall(r'\b(\d+(?:\.\d+)?)(b)\b', cleaned)
    if word_matches:
        return float(word_matches[-1][0])
    return None


def parse_params_to_billions(params_str):
    if not params_str or not isinstance(params_str, str):
        return None
    p_str = params_str.strip().lower()
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
    unknown_size = unknown_model.get("size_gb", 0.0)
    if not known_models:
        return 1.0
    closest = min(known_models, key=lambda k: abs(k["size_gb"] - unknown_size))
    return closest["param_resolved"]


def classify_and_enhance_models(raw_models):
    processed = []
    known_pool = []
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

    for item in processed:
        if item["is_known"]:
            continue
        name_candidate = get_model_name_param(item.get("key")) or get_model_name_param(item.get("display_name"))
        if name_candidate:
            item["paramEstimate"] = name_candidate
            item["param_resolved"] = name_candidate
        else:
            item["paramEstimate"] = estimate_param_from_peers(item, known_pool)
            item["param_resolved"] = item["paramEstimate"]
    return processed


def main():
    url = f"{config.BASE_URL.rstrip('/')}/api/v1/models"
    print(f"Fetching models from {url} ...")
    try:
        resp = requests.get(url, headers=utils.get_headers(), timeout=30)
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

    enhanced = classify_and_enhance_models(raw_models)

    enhanced.sort(key=lambda x: x["size_gb"] if x["size_gb"] is not None else 0.0, reverse=config.REVERSE_SIZE)
    enhanced.sort(key=lambda x: str(x.get("display_name") or x.get("key") or "").lower(), reverse=config.REVERSE_NAME)
    enhanced.sort(key=lambda x: x["param_resolved"], reverse=config.REVERSE_PARAMS)

    output = []
    for m in enhanced:
        clean = {k: v for k, v in m.items() if k not in ["is_known", "param_resolved"]}
        output.append(clean)

    utils.save_json(config.MODELS_PATH, output)
    print(f"Wrote {len(output)} models to {config.MODELS_PATH}")
    print("This replaced the active model list with the models currently in LM Studio.")
    print("Hand edits in that file are not kept. Edit it again after this refresh if you want to test a smaller set of models.")


if __name__ == "__main__":
    main()
