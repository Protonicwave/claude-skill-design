# Recording the user's design corrections

Scope note: gathered on 24 November 2026 for the corrections section of `SKILL.md`. The idea of turning corrections into rules with reasons in a project's `DESIGN.md` comes from Emil Kowalski's `learn-taste` (github.com/emilkowalski/skills, MIT), read at commit 64eb3de. It is restated in our own words, and no text is copied into the skill. Quotations below are its words, for the record.

## Q1. How does learn-taste record a correction?

### Takeaway
It reads a finished session for corrections, proposes rules with reasons, and writes only those the user approves.

### Cited findings
- "If it isn't written down, the next session makes the same mistake and the user corrects it again": [learn-taste](https://github.com/emilkowalski/skills/blob/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c/skills/learn-taste/SKILL.md).
- Sources: explicit corrections, silent edits, repeated nudges ("Record where they landed, not the steps"), rejections, and confirmed choices a fresh agent might not repeat: [learn-taste](https://github.com/emilkowalski/skills/blob/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c/skills/learn-taste/SKILL.md).
- "Skip what isn't taste: functional bugs, content specific to one screen", and corrections to the agent's understanding of the task: [learn-taste](https://github.com/emilkowalski/skills/blob/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c/skills/learn-taste/SKILL.md).
- Level: its example moves from one pricing card (too narrow) to all raised surfaces (right) to "Never use borders" (too broad): [learn-taste](https://github.com/emilkowalski/skills/blob/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c/skills/learn-taste/SKILL.md).
- "Never invent a why": a reason the user did not give is marked inferred and confirmed before writing: [learn-taste](https://github.com/emilkowalski/skills/blob/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c/skills/learn-taste/SKILL.md).
- An existing rule that failed is made stricter rather than repeated, and a conflict goes to the user: [learn-taste](https://github.com/emilkowalski/skills/blob/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c/skills/learn-taste/SKILL.md).
- Each entry keeps the date and the user's words, so a later conflict shows which is newer: [learn-taste](https://github.com/emilkowalski/skills/blob/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c/skills/learn-taste/SKILL.md).

### Inferences
- The test for an entry is whether a fresh session would make the same mistake on another part of the project. That excludes bugs and one-screen content.

## Q2. Which parts are our own?

### Takeaway
The skill records each correction when it is made, without a separate command, and reads the file before its next brief.

### Inferences
- `learn-taste` runs only when asked, and its users must point an agent file at `DESIGN.md`. web-ui-craft reads the file itself in step 1, so it needs no pointer.
- Recording in the same turn removes the approval step. The safeguards are that the reply names the entry, an inferred reason is marked and put to the user, and entries hold only what the user expressed.
- A newer contradicting correction replaces the old entry rather than being put to the user as a conflict, because the user has just said which one they want.
- A correction outranks the brief because the tests in step 3 remove choices that were nobody's decision, and a correction is the user's.
- The report line for corrections follows round six, where a rule in a reference alone did not change what builders did (`bench-round-6.md`, section 2).
- `learn-taste`'s lint-rule proposals and prune mode are left out: no recorded need for either.

### Gaps
- Hand edits are found only when the session sees that a file changed. Nothing diffs earlier sessions' output.
