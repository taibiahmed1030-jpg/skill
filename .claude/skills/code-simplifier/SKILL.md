---
name: code-simplifier
description: "Paste a function. Get back the same logic in half the lines. Removes accidental complexity without breaking behaviour."
---

Review the code just written and simplify it without changing behavior.

Steps:
1. Read all files that were modified in this session
2. For each file, identify:
   - Unnecessary abstractions (helpers used once, over-engineered patterns)
   - Redundant comments or dead code
   - Variables that could be inlined
   - Functions that could be collapsed
   - Any code that was added "just in case" but isn't used
3. Simplify ruthlessly: the goal is minimum lines for correct behavior
4. Do NOT change public interfaces, exported types, or behavior
5. Do NOT add new features, docstrings, or error handling that wasn't there
6. After simplifying, re-read the result and confirm it still makes sense

Guiding principle: if you can delete it without breaking anything, delete it.
