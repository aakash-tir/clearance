# Learning mode (required for all development)

This is a portfolio project. The owner must be able to explain every file, every line
and every test in an interview. Speed is secondary. Follow these rules in every session.

## Before writing code
1. Read the issue and its "What you will learn" line.
2. **Explain the plan first, in plain language:** what you'll build, which files you'll
   touch, and any new concept (add it to `docs/learning/concepts.md` if missing).
3. **If there's a real design choice** (library, data shape, algorithm, where logic
   lives), lay out 2–3 options with trade-offs and **ask the owner** before choosing.
   Obvious defaults: state them and proceed.

## While writing code
- One concept per PR. If the change grows past one concept, stop and split it into a
  new issue.
- Prefer explicit over clever: named variables, small functions, no magic.
- Docstrings and comments say **why**, not what.
- Build in small steps, running the tests after each step, so each step can be explained.

## After writing code: the explanation (required)
In the reply to the owner **and** in the PR body (the template has the sections):

1. **Every changed file:** what it does, why it's needed, how it fits the rest.
2. **Every test:** what behaviour it checks, which bug or leak it would catch, and why
   it's written that way (why this input, why this assertion). Add each test to
   `docs/learning/test-guide.md` in the same PR.
3. **Every correction:** if something failed along the way (test, type check, CI), say
   what was wrong, the evidence (error text), and why the fix works. Never fix silently.
4. **Walkthrough:** for anything non-trivial, trace one concrete example through the code
   (e.g. "HR user asks about Q3 revenue: here is each step").
5. **Check understanding:** end with 2–3 short questions the owner could be asked about
   this change in an interview.

## End of each milestone
Write `docs/learning/mN-<name>.md`: a one-page recap of what was built, the concepts,
how the pieces connect, and what to revise.

## Tests (security project, so extra care)
- Every test must be able to fail. When adding a test, show it failing first where
  practical (red → green).
- Leak tests (`@pytest.mark.leak`) assert both sides: the allowed persona *can* see the
  document, and every other persona *cannot*.
- Never weaken or delete a leak test to make CI green. If a leak test fails, that's a
  security bug: stop and explain.
