# Expense Tracker Dashboard

Build a single-page React + TypeScript expense tracker. Use only functional components and hooks. Do not use any external UI or chart libraries.

## Data Model
Define a TypeScript interface for an Expense with these fields:
- id: string
- amount: number
- category: string
- date: string (ISO format)
- description: string
- notes?: string

Start the app with 5 realistic sample expenses already loaded in state.

## Required UI
The main view must contain:

1. Summary section at the top with three cards:
   - Total amount spent
   - Highest spending category
   - Number of expenses

2. Filter controls:
   - Dropdown to filter by category (include an “All” option)
   - Date range inputs (from / to)

3. List of expenses that respects the current filters. Show amount, category, date, and description for each item.

4. A form to add a new expense. Validate that amount is greater than 0 and that category, date, and description are filled in. Clear the form after a successful add.

5. Clicking any expense opens a detail panel (or expands the row) where the user can:
   - Edit any field
   - Delete the expense
   - Close the panel

## Technical Requirements
- All state lives in React (useState or useReducer).
- Extract at least these components into separate files:
  - SummaryCards.tsx
  - ExpenseFilters.tsx
  - ExpenseList.tsx
  - ExpenseForm.tsx
  - ExpenseDetail.tsx
- Keep App.tsx as the main orchestrator.
- Make the layout usable on a narrow window.
- Add basic accessibility (labels on inputs, keyboard-focusable buttons).

## Deliverables
Produce the complete set of files needed to run the app, plus a short README.md that lists the files and how to start it with a standard Vite + React + TypeScript setup.