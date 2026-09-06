---
title: Third-party notices
doc_type: notice
module: coding-agent-system
topic: third-party-licences
status: stable
created: 2026-08-29
updated: 2026-08-29
owner: self
source: human+ai
---

# Third-party notices

This project reviewed, but did not install or vendor, the following MIT-licensed skill repositories on 2026-08-29:

- [mattpocock/skills @ 6654f6b](https://github.com/mattpocock/skills/tree/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76), Copyright (c) 2026 Matt Pocock.
- [vinvcn/mattpocock-skills-zh-CN @ 9fb0161](https://github.com/vinvcn/mattpocock-skills-zh-CN/tree/9fb0161ac2be0c45c59cbea0878eb77d92cc24b5), whose local `LICENSE` states Copyright (c) 2026 Matt Pocock.

The current project files contain independently written research, decisions and selective skill rewrites. They do not reproduce complete third-party skills. If a future change copies a substantial portion of either repository, retain the applicable MIT copyright and permission notice with that copied material.

The fixed commits, repository URLs, licence records and per-skill decisions are in [third-party-skills.lock.json](third-party-skills.lock.json).

## Research-method source with unresolved licence text

This project also reviewed [karpathy/autoresearch @ 228791f](https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117) as method inspiration. Its pinned `README.md` labels the project `MIT`, but the pinned repository contains no `LICENSE`, `LICENSE.md`, `LICENSE.txt`, `COPYING`, or equivalent licence text, and GitHub reports no detected licence metadata.

The Coding Agent system only cites and independently restates the general idea of a bounded edit-run-measure-keep/discard experiment loop. It does not copy `prepare.py`, `train.py`, `program.md`, datasets, logs, or performance claims, and it does not rely on the README label as a verified grant to reuse code or long-form instructions. The fixed commit, evidence boundary and adapt/exclude decision are in [research-methods.lock.json](research-methods.lock.json).
