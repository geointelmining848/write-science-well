# write-science-well

An Agent Skill that teaches an AI assistant to write, revise, diagnose, and plan scientific
prose the way four books teach it: Strunk's *The Elements of Style*, Zinsser's *On Writing
Well*, Alley's *The Craft of Scientific Writing*, and Heard's *The Scientist's Guide to
Writing*. Every rule names its book, so the assistant can weigh it and you can check it.

It works in Claude Code, Codex, Kimi Code, Cursor, and any other agent that reads the open
`SKILL.md` format. Install it once, then ask the way you would ask a colleague: "my coauthor
says section 3.2 reads badly, tighten it without changing the model", "should the Methods be
in the passive voice?", "tell me what is wrong with this discussion before I rewrite it".

## What is in it

The skill holds the books' rules in ten reference files, read on demand so a session loads
only what the task needs. It also holds thirteen rulings for the places where the books
disagree (hedging, the passive, first person, sentence-initial "However", bullets, dashes,
how an introduction ends, how much the Methods carry, conclusions, repetition, titles,
technical terms), each with its reason.

| File | What it carries |
|---|---|
| `SKILL.md` | The four principles, the four modes, output formats, the thirteen rulings, what is out of scope, a twelve-question checklist |
| `references/structure.md` | The story, IMRaD parts, titles, abstracts, introductions, methods, results, discussions, proposals, reports, theses, book chapters, headings, emphasis |
| `references/paragraphs.md` | Paragraph unity, topic sentences, sentence-to-sentence links, paragraph length, lists in prose |
| `references/sentences.md` | Sentence length, word order, voice, tense, first person, pronouns, parallel form, punctuation, the usage watchlist |
| `references/words.md` | Clutter, hedges, intensifiers, nominalizations, concrete words, jargon, abbreviations, numbers in text |
| `references/revision.md` | Single-purpose revision rounds, reader simulation, cutting, reading aloud, proofreading |
| `references/process.md` | Starting, momentum, outlining, fear, writing in English as an additional language |
| `references/figures-tables-equations.md` | Tables, figures, captions, legends, pointing at graphics, equations |
| `references/review-and-coauthors.md` | Friendly and formal review, responses to reviewers, writing a review, coauthors |
| `references/house-style.md` | Your own standing preferences, with an editable starter set |
| `references/sources.md` | The four books, what each contributes, what was left out, the rulings with reasons and pages |
| `scripts/prose_signals.py` | A standard-library scanner that reports prose signals on a text, Markdown, or .docx file |
| `evals/` | Three test tasks with their expected behavior, in the Claude Code skill-creator format |

The books are the source. The skill paraphrases their rules with the author's name and, in
the reference files, the page; it quotes a few short passages with attribution and
reproduces no book. Strunk's 1918 text is in the public domain. The other three are in
print, and the skill is a reason to read them, not a substitute.

## What it does

The skill works in four modes and picks the one your request implies.

- **Draft**: new text from notes, an outline, or results. It finds the story first, takes
  the skeleton for the document part from the books, writes only what your notes support,
  and lists the gaps instead of inventing a bridge.
- **Revise**: text you supply. It chooses the scale of the edit from your request (a named
  fault gets a surgical fix; "make it stronger" gets proposed deletions and moves as
  reversible items), revises in single-purpose rounds, and verifies that no number, claim,
  citation, or term drifted.
- **Diagnose**: ranked findings with no rewrite, substance before mechanics. Each finding
  quotes the words, names the rule and its author, and says what a fix would do.
- **Plan**: audience, purpose, occasion, the two-sentence summary, the figures first, the
  skeleton, a topic-sentence outline, and the power positions marked.

Manuscript prose comes back paste-ready: plain text, one line per paragraph, no Markdown,
no em dashes, with a landing anchor that says what it replaces. Every revision carries a
change list that names the rule behind each change, and a cut list for every deleted
sentence. The skill never invents a number, a citation, a result, a claim, or a venue's
word limit.

## Install

Pick one way per agent. Installing the skill twice in one agent makes it trigger twice.

### Claude Code

As a plugin, in one step on Claude Code 2.1.275 or later:

```
/plugin install write-science-well --marketplace geointelmining848/write-science-well
```

On an earlier version, add the marketplace first and then install from it:

```
/plugin marketplace add geointelmining848/write-science-well
/plugin install write-science-well@write-science-well
```

Or as a personal skill, available in every project:

```bash
git clone https://github.com/geointelmining848/write-science-well ~/.claude/skills/write-science-well
```

On Windows the folder is `%USERPROFILE%\.claude\skills\write-science-well`. Start a new
session after installing. To update a cloned copy, run `git pull` in that folder.

### Codex, Cursor, Kimi Code, and other agents

The `skills` installer puts the skill in the right folder for the agents you name, or for
every agent it finds on your machine:

```bash
npx skills add geointelmining848/write-science-well
```

Or copy by hand. Clone the repository into the folder your agent reads, under the name
`write-science-well`: Codex reads `~/.codex/skills/` and `~/.agents/skills/`, Kimi Code
reads `~/.kimi-code/skills/` and `~/.agents/skills/`, Cursor reads `~/.cursor/skills/`.

### claude.ai and the Claude desktop app

Download the repository as a zip (Code, then Download ZIP). Then open Settings,
Capabilities, Skills, and upload the zip.

The skill then runs in chat the same way, except that the signals script needs a code
sandbox to run.

### Any other assistant

Paste the body of `SKILL.md` (everything below the second `---`) into the system prompt or
custom instructions, and attach the reference files the task needs.

The method is plain text. Any capable model can follow it, with or without a skills loader.

## Use it

The skill triggers on ordinary requests about scientific text. Some that work:

- "Here is the abstract of my chapter. Make it a stronger abstract, keep every claim and
  term, and give it to me paste-ready for Word."
- "Section 3.2 of our paper is about 900 words on the estimation strategy and my coauthor
  says it is unreadable. Tighten it without changing the model."
- "Read this results section and tell me what is wrong with it before I rewrite it. Do not
  rewrite it; rank the problems."
- "Should I write the Methods in the passive voice? My advisor insists; the paper I am
  modeling on uses 'we' throughout."
- "Draft our reply to reviewer 2, who says the 5 km threshold is arbitrary. We added a
  sensitivity check at 3 and 8 km and the results hold."
- "How should I structure the project description for a 15-page proposal with three aims?"

Attach the text or name the file. For a .docx file the skill extracts the text, works on
it, and returns paste-ready prose; it does not edit the file in place unless you ask.

## Make it yours

`references/house-style.md` is the layer between your live instructions and the books, and
it wins when the two conflict. It ships with a starter set learned in live revision
sessions on real papers and chapters: paste-ready delivery with landing anchors, no em
dashes, no one-paragraph sections, every example introduced before use, write the science
rather than the software, no provenance tag on every mention, literal over figurative,
certainty for designed behavior and hedges only for what the analysis leaves open.

Delete the rules you do not hold, add your own with their reasons, and fill in the last
section, "The author's voice", with the phrases and habits an editor must leave alone in
your text. Nothing else in the skill needs to change.

## The signals script

`scripts/prose_signals.py` reads plain text, Markdown, or .docx and reports sentence
lengths, passive candidates, expletive openers, nominalizations, clutter phrases from the
four books, hedges, intensifiers, bare sentence-initial "this", noun strings, em dashes,
one-use acronyms, and echoed words. It uses only the Python standard library and never
touches the network.

```bash
python3 scripts/prose_signals.py draft.docx
python3 scripts/prose_signals.py section.txt --json --top 10
python3 scripts/test_prose_signals.py
```

The header says what it is: signals, not verdicts. A Methods section can run high on
passives and be right. The skill runs the script at most twice per task, once to decide
where to read first and once on its final text.

## How it was tested

The skill was built with Claude Code's skill-creator and run through three rounds of its
benchmark: the same tasks with and without the skill, graded on written assertions by a
separate model, with the author reviewing a sample of the outputs. The tasks were to
tighten a cluttered methods-and-results paragraph, draft an introduction from notes,
diagnose a discussion section, and strengthen a book-chapter abstract.

| Round | Assertions | Passed with the skill | Passed without |
|---|---|---|---|
| 1 | 39 | 39 | 31 |
| 2, harder set | 45 | 40 | 34 |
| 3, final | 46 | 45 | 34 |

The score mattered less than the kinds of fault. In every round the runs without the skill
added claims the source did not carry. The early rounds also caught faults in the skill's
own output (a placeholder left in paste-ready text, a diagnosis of two thousand words, a
venue word limit stated without a source), and the instructions were changed until the
final round showed none of them. The test set is small and the grader is a model, so treat
the numbers as a smoke test, not a measurement. The fourth task used an unpublished chapter
abstract, so this repository ships the three synthetic tasks only.

## Contributing

Open an issue or a pull request. A new rule needs its book, its page, and its reason, in
the reference file for its layer; a rule with no book behind it goes in the house-style
file, marked as a preference. Keep em dashes out of every file except inside exact
quotations.

Before a pull request, run the script's self-test and read `SKILL.md` on its own, because
that file is all the agent sees until it opens a reference.

## License

MIT, copyright 2026 geointelmining848. The four books belong to their authors and publishers.

Built with Claude Code.
