## Task prompts

Instead of maintaining separate, verbose prompts for each feature, use `docs/tasks.md` as the single source of truth for current work.

- **Step 1 – Pick a task**: Open `docs/tasks.md` and choose an item from the **Remaining (prioritized)** section (starting with High priority).
- **Step 2 – Turn it into a prompt**: Wrap that task in a short instruction like:
  - “Implement this task in code, following the project devguide and safety rules: \<paste the task line from `docs/tasks.md`\>.”
  - “Refine tests and docs for this task: \<paste the task line from `docs/tasks.md`\>.”
- **Step 3 – Keep docs in sync**: When you complete a task, update the checkbox in `docs/tasks.md` and, if needed, adjust the description so it accurately reflects what was done.

This keeps prompts and the task list aligned while preserving the prioritization in `docs/tasks.md`.


