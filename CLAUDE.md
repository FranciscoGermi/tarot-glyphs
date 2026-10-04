# Tarot Glyphs

A study of the tarot, and tools built on it: card scans, their history, symbolism and meanings, crawled
and read from primary sources, then printed in code page 437 glyphs with the technology from
after-what-i-did. **It starts as a study and tests.** The likely product is a reading app on the web with
a phone layout, with animated glyph cards; the runtime (web shader, three.js, or the C++ engine) is
**not decided** (`DECISIONS.md` §1).

## Reading order

**Start at `STATE.md`.** Only this file is auto-loaded.

| file | read it when |
|---|---|
| **`STATE.md`** | **Always, first.** What exists, what is next, what is open. Capped near 250 lines. |
| **`DECISIONS.md`** | Before proposing anything that might already be settled, or when you need the reason behind a decision. |
| **`PORT.md`** | Taking anything from after-what-i-did. Deleted when the port is done. |
| **`PLAN.md`** | Picking the next step. The order of the work ahead; deleted when its last step is done. |
| **`research/`** | A study exists for a question before you answer it from recall. |
| **`THIRD_PARTY_LICENSES.md`** | Before anything crawled or borrowed is shipped, printed or published. |

`py tools/sec.py DECISIONS` lists every section number and title; `py tools/sec.py DECISIONS 2 3`
prints those two.

**There is no `HISTORY.md`, and no document is append-only.** `DECISIONS.md` is **edited in place to
current truth**: a superseded decision is removed rather than annotated. `git log -p` is the archive.

**Procedures are skills, not documents.** `.claude/skills/` holds how to *do* a thing; the files above
hold what is *true*. **Findings never go in a skill**: they belong in `research/` or `DECISIONS.md`.

## Starting and ending a session

**To resume, Francisco says: `read STATE.md and continue`**, optionally naming what he wants.

**To close, Francisco says: `handoff`.** That means:

1. **Rewrite `STATE.md` in place**, never append a dated block.
2. **Keep it near 250 lines.** If it overflows, something graduates to `DECISIONS.md` or a study.
3. **Update `DECISIONS.md`** with anything actually decided and its one line of reason, in the section
   it belongs to, deleting what it supersedes.
4. **Report what was not finished** and what is un-judged. An accurate handoff beats a tidy one.
5. **Name the effort level the next step wants, and why.** Mechanical work runs at medium; high is for
   a step with an undecided design in it. **Do not switch effort mid-session.** A step that needs both
   is two sessions. **The session runs at the effort he launched it with.**

**To run work unattended, Francisco says: `goadv`**, or `goadv on <what>`:

1. The named work (bare `goadv`: `PLAN.md`'s next step onward) is approved as a whole.
2. If the session has no advisor, say so and stop.
3. Run it as a self-paced `/loop`, one step a round. Each step's plan goes to the advisor instead of to
   him (rule 15). Commit after each step; never push.
4. Stop for him at a step he must judge, where the advisor and a measurement disagree and the plan
   does not settle it, or at the end. Report what was and was not done.

**To settle what can be settled now, Francisco says: `askop`**, or `askop on <what>`: find every open
decision in the named work and put each one he can answer to him as option questions, batched, the
recommended option first (rule 16).

**To close a session for a fresh one, Francisco says: `wrapup`**: commit finished, verified work (rule
18's check first), do the whole `handoff`, commit the documents, never push, and reply with what was
committed, what was not finished, and the effort the next session wants.

**Do not commit or push unless asked**, except inside `goadv`.

## The working agreement

**1. Every build step goes through plan mode first.** Under `goadv` the advisor approves each step's plan.

**2. Go to the primary source.** Read the actual scan, book, repository or specification. Do not work
from recall about a card's meaning, a deck's history or a library's API: tarot writing is full of
repeated claims nobody checked. Quote where a claim came from (book, edition, page) so it can be checked.

**3. Write your own findings.** Independent analysis, not a restatement of what Francisco already said
or of what the most-copied website says.

**4. Say what you could not determine.** Every study ends with an explicit list of what remains
unknown. Do not inherit a claim from another source as if it were verified. Distinguish a real negative
from a broken measurement, and a documented fact from occult tradition, and say which it is.

**5. Instrument before you change.** If you do not know why something looks or behaves wrong, form a
hypothesis, build a test, measure, look, then decide.

**6. Ask for what you need instead of working around it.** A missing tool is asked for in one sentence.

**7. A comment block is 2 lines at most, and says why — never what.** No dates, history, decisions or
document citations in source. `py tools/comment_cap.py` enforces it in the pre-commit hook.

Between *documents*, citing `DECISIONS.md` by section is fine, but **its numbering is not stable across
a rewrite**. **`STATE.md` and `PORT.md` are never cited by section from anywhere.**

**8. One owner per fact.** Never restate a flag, a default, a version or a run line in prose.

**9. Use the session scratchpad for temporary work**, never the project folder.

**10. Study material is kept and gitignored.** Findings stay tracked; scans, PDFs and pixels do not.
Anything ignored must be regenerable, so record the command that made it.

**11. A reply is not a document.** Answer in the fewest words that carry the fact and stop. Status
updates are one or two lines. **This stops at the documents**: in `STATE.md`, `DECISIONS.md` and
`research/`, rules 3 and 4 still demand the hedge, the negative result and the list of unknowns.

**Reads cost the same way.** Grep for the anchor, then read only those lines. Never re-read a file
already in context, and send long command output to a file and print only the summary.

**12. Ask the owner to look when that is cheaper than the instruments.** Judgment (does this read
right, is this the feel) goes to a person; correctness goes to the instruments. Hand over the exact
command or URL and the one question being asked. **A run line is one self-contained PowerShell line**
with absolute paths.

**13. Design is held to the same standard as code.** Colour, readability, animation and card layout
are technical disciplines with a literature: study it and cite it, work from references, and judge the
result in captures and in motion. The aim is the illusion, not the detail.

**14. The critic loop.** Once there is a look to judge, every step that changes how a card looks or
reads passes a fresh blind critic before Francisco sees it. The skill comes over from after-what-i-did
with the first capture worth judging (`PORT.md`).

**15. Every session has the advisor** (he turns it on with `/advisor`). Consult it before leaving plan
mode, when a measurement contradicts the hypothesis a second time, and before handing Francisco
something to judge in motion. Where its advice conflicts with a measurement, the measurement wins and
the conflict is reported.

**16. At a real fork, ask with options; inside an agreed direction, decide.** A design choice or a
scope call goes to him as option questions, batched, the recommended option first. A "safe" default
swapped in for the asked-for one is a decision too: say it.

**17. The tools on this machine.** PowerShell is the shell; Python is `py` (bare `python` is 2.7). In
Git Bash set `PYTHONUTF8=1`: code page 437 output does not survive cp1252. **Source, tool and document
edits go through Edit or Write**, never shell text tools. The hook needs `git config core.hooksPath
.githooks` once per clone.

**18. Nothing outside this repository sets how work is done here.** No standing rule lives in Claude's
memory folder; it goes in this file, after he agrees. Installs and sign-ins are asked for each time.
**A commit is verified before it is made.** History is never rewritten to look incremental.

**19. Crawl politely, and record the licence before using the take.** A crawler sends a real Referer,
pauses between requests, resumes instead of re-fetching, and writes a manifest (URL, size, SHA-256,
date). What a source allows is read from the source itself and recorded in `THIRD_PARTY_LICENSES.md`
with the date read; until then its column says unknown and nothing of it leaves this machine.

## Conventions

- Research documents are `Title — Subtitle.md` with an em dash, opening with **In brief** and closing
  with **What remains unknown** and **Reproducing**.
- Git identity is `Francisco Germi <psuarez.francisco@gmail.com>`, from the global config: never set
  `user.name` or `user.email` in this repo. Commit messages are one title under about 60 characters and
  no description.
- **Never name a real person, client or brand in anything shareable**, except public creators and works
  cited in research and the credits a licence demands (Pamela Colman Smith, A. E. Waite, Yoav Ben-Dov,
  VileR for the fonts).
