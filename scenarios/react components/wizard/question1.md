# Multi-Step Controlled Wizard

Build a three-step React + TypeScript wizard. Use only functional components and hooks. No external libraries.

## Steps
1. Basic info — name (required, min 2 characters) and email (required, must contain @).
2. Preferences — two checkboxes (newsletter, notifications) and a select for preferred contact method (email, phone, none).
3. Review — show a read-only summary of all values and a Submit button.

## Requirements
- All inputs must be controlled with React state (`useState` or `useReducer`).
- Keep the current step and all form data in the parent component.
- Next button is disabled until the current step passes validation.
- Back button works on steps 2 and 3 and does not lose data.
- After submit, show a simple success message (no real API call).
- Extract small presentational components if it keeps the code clean, but the parent owns the state.
- One main file is fine (for example `Wizard.tsx`).

## Deliverables
Produce the complete component code plus a short note on how to drop it into a standard Vite + React + TypeScript app.
