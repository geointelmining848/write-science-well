---
name: write-science-well
description: >-
  Write, revise, diagnose, or plan scientific prose the way Strunk, Zinsser, Alley, and
  Heard teach it: journal papers, book chapters and monographs, grant proposals, theses,
  titles, abstracts, cover letters, responses to reviewers, and reviews. Use this skill
  whenever the user wants scientific or technical text drafted or tightened, says a passage
  is dense, wordy, unclear, flat, or reads badly, wants paste-ready revisions for Word, asks
  what is wrong with a section, asks how to structure a paper or chapter, or asks about a
  writing rule (active or passive, first person, hedging, starting with because), even when
  they name no book and never say "skill". Covers writing process, document structure,
  paragraphs, sentences, words, figures and tables, revision, review, and the author's own
  standing preferences through an editable house-style file. Not for citation mechanics and
  reference managers, venue selection or peer-review simulation, developmental editing of a
  whole monograph, or agent-to-user chat.
---

# Write Science Well

This skill distills four books on writing: Strunk, *The Elements of Style* (1918/1920);
Zinsser, *On Writing Well* (2001 ed.); Alley, *The Craft of Scientific Writing* (4th ed.,
2018); and Heard, *The Scientist's Guide to Writing* (2016). Every rule in the reference
files comes from one of them, with the author named, so you can weigh it and the reader can
check it. The books agree on the goal: prose so clear that the reader never notices it.
Heard calls that telepathy. Alley's law is Einstein's: as simple as possible, yet no simpler.
Zinsser's method is subtraction. Strunk's is "omit needless words."

## Four principles every rule serves

1. **The reader's effort is the only measure.** If the reader is lost, the writer was not
   careful enough (Zinsser). Settle every craft question by asking which choice lets the
   reader understand the story more easily (Heard). Analyze who reads, why, and what they
   already know before choosing a word (Alley).
2. **Say what you mean and nothing you do not mean.** Precision and clarity pull against
   each other; needless complexity is the most common failure in scientific prose (Alley).
   Hedge exactly to the evidence, and inflate nothing (Heard, Alley).
3. **Every word earns its place.** A sentence should contain no unnecessary words, a
   paragraph no unnecessary sentences (Strunk). Most first drafts can lose half their words
   without losing information (Zinsser). Force every character to justify itself (Heard).
4. **Fact and deduction, in a line.** Scientific writing is one sentence after another, and
   the "after" is what makes it hard (Zinsser). One idea per sentence, actor next to
   action, the new information at the end (Alley, Heard, Strunk).

The reasons behind the rules matter more than the rules. When a rule and the reader's
interest conflict, the reader wins, and the reference files say why each rule exists so you
can judge the exception.

## Start here, every time

1. **Name the mode.** Draft (produce new text), Revise (rewrite supplied text), Diagnose
   (rank what is wrong, no rewrite), or Plan (design the document before drafting). Pick the
   one the request implies; say which you chose only if it was unclear.
2. **Fix audience, purpose, occasion** (Alley). Who reads this, why, what they know, and what
   the venue allows in length and form. A journal page limit gives a claim one sentence of
   justification; a report or chapter gives it a paragraph.
3. **Load what you need, and only that.** `references/house-style.md` first, every time (it
   is short): it holds the author's standing preferences, with a starter set the author can
   edit. Then the files the mode needs, from the reading list in the reference map below.
   The files carry tables of contents; read the sections the task touches, not every file
   end to end.
4. **Run the signals script twice at most**: once on any supplied text longer than a
   paragraph, before reading closely, and once on your final text before delivering:
   `python3 scripts/prose_signals.py <file>` (or `--json`). It reports sentence lengths,
   passive candidates, expletive openers, nominalizations, clutter phrases, hedges,
   intensifiers, bare sentence-initial "this", noun strings, em dashes, and one-use
   acronyms. The header says what it is: signals, not verdicts. Use it to decide where to
   look first, then read.
5. **Decide what must not change.** Numbers, claims, citations, defined terms, and, when the
   text is the author's own, the argument turns and voice the house-style file protects.
   Never invent a number, a citation, a result, or a claim the source does not carry. Mark a
   gap as `???` and list it.

## Mode: Draft

Drafting from notes, an outline, or results.

1. **Find the story first.** Write the two-sentence mini-summary: the central question and
   its answer (Heard). It settles what belongs: would including this help tell the story or
   distract from it? For a book section, state the reader question the section answers and
   that the chapter does not already answer (house style). If the notes carry no answer, the
   story is the question plus the design, and you say so.
2. **Take the skeleton from `references/structure.md`.** An introduction moves from
   territory to gap to what this work does, and ends on the question, the approach, and the
   main result (Heard); the opening breadth is set by the venue. An abstract is an
   informative summary that gives the result away (Alley, Heard). A discussion answers the
   question in its first paragraph and ends on the most important finding and its
   significance (Heard). A chapter opens with an orienting sentence and maps its sections
   (Alley, house style).
3. **Decide the unities before writing** (Zinsser): the pronoun, the tense, the tone. Hold
   them to the end.
4. **Draft fast, then revise in order.** Storm the beach with a complete draft, placeholders
   for anything missing (Heard). Then run the Revise rounds below on your own draft before
   delivering. The reader sees only the revised draft.
5. **Write only what the sources support, and keep gaps out of the paste-ready text.** Do
   not add a claim, a mechanism, or a consequence the notes do not carry, even to bridge an
   argument ("planting vegetation can cool a neighborhood but cannot raise its income" is a
   claim, not a transition). Bridge with the notes' own facts, or leave the seam and flag
   the gap in the note; disclosing an added claim does not make it admissible. When the
   notes carry no main result, end an introduction on the question and the approach (the
   order Heard names as the alternative) rather than on a placeholder; the note says what
   a closing result sentence would add. A priority claim ("the first to test") keeps
   its qualifier ("to our knowledge"), because the literature search is what the analysis
   cannot settle (house style: hedge what genuinely remains unresolved).
6. **Deliver** the text in the requested form (paste-ready for manuscript prose; see Output
   formats) plus a short note listing gaps, assumptions, and the one or two choices the
   author may want to reverse (for instance "the draft ends on the design; if you want it
   to end on the main result, add one sentence: …").

## Mode: Revise

Tightening or clarifying text the user supplies. This is the mode a coauthor's "it reads
badly" calls for.

1. **Read the whole passage once for its story and the author's intent** before touching a
   word. Note the non-negotiables from "Start here".
2. **Choose the scale of the edit from the request, and say which you chose.** Three cases:
   - A request to fix a phrase, or a chapter the author has finished: revise the exact phrase
     or sentence, and report only factual or scientific errors elsewhere (house style).
   - A request to strengthen, improve, or make a passage read well, including the author's
     own text: do all three of the following, and report each. First, the value test: name
     any sentence that carries no claim (a self-announcement such as "This chapter sets out
     why…", a recap, a caveat that changes no claim, a chapter map inside an abstract) and
     propose its deletion as a reversible item, with the sentence quoted and the reason;
     if you keep such a sentence, say why. Second, the structural move that would help most
     (a sentence moved to where its consequence follows, a buried finding brought forward,
     four parallel sentences folded into one), proposed the same way. Third, the phrase
     repairs: an ambiguous connective ("since" for "because"), a pronoun or "those" with no
     clear referent, a figurative verb, a doubled phrase now sitting in adjacent sentences.
     "Keep every claim and term exactly" forbids new claims and renamed terms; it does not
     forbid these repairs, which change no claim. Never rewrite a whole paragraph for style
     alone, and keep the author's voice, terms, and claims.
   - A request to tighten a draft: rewriting is licensed, but every fact, number, term, and
     citation survives unchanged.
   A real review of this skill made the middle case explicit: asked for a "strong"
   abstract, the author preferred the revision that moved a sentence over the one that
   changed three phrases and left the structure alone.
3. **Revise in single-purpose rounds, in this order** (Heard, Alley), because you should
   never polish what you are about to cut:
   - Content: cut what does not serve the passage's job; check the claim matches the
     evidence; keep only hedges the evidence needs.
   - Structure and paragraphs: one point per paragraph, announced early; each sentence
     begins in a way that connects to the one before; the new, important item sits at the
     end of the sentence and the paragraph (`references/paragraphs.md`).
   - Sentences: actor next to action, verb early, one idea per sentence, active unless the
     passive does one of its three jobs, no bare "this", no dangling modifier, no ambiguous
     pronoun (`references/sentences.md`).
   - Words: clutter phrases, nominalizations, intensifiers, stacked hedges, jargon the
     reader does not hold, numbers reported to needless precision
     (`references/words.md`). An abbreviation used once in the passage is spelled out in
     the text itself, not left in place with a note; if it recurs later in the document,
     say so in the note and keep the definition.
   - Mechanics: commas after introductory phrases, serial commas, no em dashes, tense
     consistent within the section, acronyms defined once.
4. **Simulate the reader** (Heard). Read the revision as a stranger who has only the words.
   Read it aloud in your head for the links between sentences (Zinsser).
5. **Verify nothing drifted.** Every number, unit, interval, citation, and defined term is
   identical to the source. Claims are neither stronger nor weaker than the source made them
   unless the user asked for that change.
6. **Deliver** paste-ready text, a change list, and, when you cut sentences, a cut list (see
   Output formats).

## Mode: Diagnose

Ranked findings without a rewrite. Also the mode for "why is this wrong?" and "should I use
the passive here?": name the rule, the author, the reason, and one before-and-after example
from the reference files.

1. Run the script; read as the intended reader; keep the whole document's story in view.
2. **Rank findings by their cost to the reader**, substance before mechanics: the story and
   the claim (an overclaim, a missing boundary, evidence that does not support the
   interpretation, a buried main finding) first; structure (order, power positions, missing
   links, a recap where an ending should be) second; paragraphs third; sentences fourth;
   words fifth; mechanics last.
3. **Write each finding in one shape:** quote the offending words (five to twelve of them),
   say what goes wrong for the reader, name the principle and its author, and say what a fix
   would do. Group repeated mechanical faults into one finding with a count.
4. **Keep the whole diagnosis to about 800 to 1,200 words for a section**, and at most
   twelve findings. The three to five findings that carry substance get a paragraph each;
   the rest get one line with a count and one quoted instance. A reader who has to work
   through two thousand words of findings will not act on any of them. Cut length from the
   mechanical findings, never from a substantive catch: a term that drifts between what was
   measured and what is claimed (proximity measured, "air pollution" claimed), a claim made
   at two strengths, a buried finding. An acronym the section never defines is always a
   one-line finding.
5. Do not rewrite unless asked. If a principle is unclear without an example, show one
   revised sentence, labeled as an illustration.
6. Close with the two or three changes that would matter most, in order.

## Mode: Plan

Designing a paper, proposal, chapter, or section before drafting.

1. Audience, purpose, occasion, venue, and length budget (Alley).
2. The two-sentence mini-summary, then the selling line: why the question matters to this
   reader, not to the author (Heard). Reject timid framings ("no studies have reported").
3. Shuffle the figures and tables first; let the question be implicit in the answers they
   give (Heard). Be reluctant to exceed about five figures and four tables in a paper.
4. The skeleton for the document type from `references/structure.md`, then a topic-sentence
   outline: one line per paragraph stating its point, in order, with the job of each section
   named.
5. Mark the power positions: the first and last paragraph of each section, the first and
   last sentence of each paragraph, the title, the headings (Alley, Heard). Put the main
   result where text borders white space.
6. List what stays out (Heard's three-way test: body, supplement, or unpublished) and the
   placeholders still to fill.

## Output formats

- **Manuscript prose is paste-ready**: plain text, one physical line per paragraph, no
  Markdown markers, no bullets, no numbering, no code fences, no hard line breaks, and no em
  dashes. The author pastes it into Word. When the text replaces existing prose, name the
  landing point: quote the first and last words to remove and say whether the replacement is
  a sentence, a paragraph, or a subsection (house style).
- **The change list** is short and grouped: what changed, the rule and its author, why it
  helps the reader. Trivia (commas, a typo) go in one line with a count.
- **The cut list** names each deleted sentence and why it went (repetition, metadiscourse,
  a caveat that changed no claim, a detail that could not change the reader's
  interpretation).
- **Findings** (Diagnose) use normal chat formatting, ranked.
- **A .docx input**: extract the text, work on it, and deliver paste-ready prose. Tracked
  changes in the file itself need a docx-editing skill or tool, and only when the user asks
  for them. Do not edit a manuscript file in place unless asked.
- **Never fabricate.** No invented numbers, citations, results, or claims, and no venue
  requirements (a word limit, a format rule, a journal's policy) unless the user or a
  loaded file supplies them; say "check the venue's limit" instead.
- **Paste-ready text carries no placeholders.** A `???` belongs in the note, with the
  sentence that would hold it, never in the text the author pastes. Draft what the sources
  support and list the gaps.

## Precedence, and where the books disagree

The author's live instruction > the project's own conventions (a style sheet, a term list,
the venue's rules) > `references/house-style.md` > these four books. Among the books, for
scientific documents: Alley and Heard
(science-specific) over Zinsser (nonfiction craft) over Strunk (usage baseline). Strunk's
dated usage rules (generic "he", shall and will, the ban on split infinitives, "however"
never first) are historical and not applied.

The rulings where the books pull apart (full reasons in `references/sources.md`):

1. Hedge exactly to the evidence; cut habit hedges; attack inflation ("prove", "optimal",
   "clearly demonstrate") as hard as caution.
2. Active by default; passive for three jobs (direct attention to the acted-on, hide an
   actor nobody cares about, avoid an unwieldy subject) and when the topic of the paragraph
   must be the subject.
3. Measured "we" as the actor; not sentence-initial by default; never to narrate drafting.
4. Sentence-initial "However" and "Because" are allowed.
5. "Data" is plural in formal prose, or sidestep with "the dataset" or "data point".
6. No bullets in manuscript prose; numbered lists belong in instructions.
7. Semicolons for two closely linked clauses, not as a habit; em dashes never.
8. A paper's introduction ends on the question, the approach, and the main result; a long
   document maps its sections instead.
9. Methods carry every detail that could change the reader's interpretation of the results
   (Heard's credibility criterion), plus whatever the venue's reporting checklist requires.
10. A paper ends its Discussion on the main finding's significance, with no separate
    conclusion unless the venue wants one; chapters, reports, and proposals close on a
    plateau that adds scope, changed claim, limits, and consequence, never a recap.
11. Repetition across parts (abstract, results, discussion) is purposeful; within a part it
    is clutter.
12. Titles: specific over short; a sentence title only where the field accepts it.
13. Technical terms when the audience holds them, defined once; jargon never as a crutch.

## Signals, not verdicts

The script reports counts and examples; a human decides. Alley's numbers (average sentence
length in the teens, paragraphs of seven to eleven lines, a reading level of 10 to 13) are
advisory targets from a book for engineers, not gates. A Methods section can run high on
passives and be right. The house-style starter rule is that sentence length follows the
chain of reasoning. Use a high signal as a reason to read that passage first, and the
reference files to decide what, if anything, to change.

## Out of scope, and hand-offs

This skill writes, revises, diagnoses, and plans the prose. The neighbors below are outside
its scope. Hand each to a skill or tool in your environment that covers it; if none does, say
so and stay within the prose.

- Schimel's story architecture (OCAR, the hourglass as he draws it) and his stickiness
  craft, from *Writing Science* (2012): not in these four books. Use a Schimel-based skill
  when the user asks for his method; for everything else this skill is the default.
- Venue selection, editor pitches, and peer-review simulation.
- Developmental editing of a whole monograph: chapter order, what each chapter must do,
  cuts and moves across chapters, a project's term list.
- Citation mechanics: reference managers, citation styles, bibliography conversion.
- Word files with tracked changes, through a docx-editing skill or tool, only when the user
  asks for tracked changes. Figure production, through plotting tools.
- Plain-language chat, memos, and emails from the agent to the user.

## Reference map

Reading list by mode (the files have tables of contents; read the sections named):

| Mode | Read | Skip unless the task raises it |
|---|---|---|
| Revise a paragraph or section | house-style; words; sentences (sections 1 to 4, 8, 10); paragraphs (topic sentence, connecting sentences); the part's section of structure (abstract, introduction, methods, results, discussion) | process, revision, review-and-coauthors, figures |
| Draft a part from notes | house-style; structure (the story, the part being drafted, emphasis); paragraphs; words (sections 3 to 5); sentences checklist | process, review-and-coauthors |
| Diagnose a section | house-style; structure (the part's section and the checklist); paragraphs, sentences, words (their checklists first, then the sections a finding needs) | process, revision, review-and-coauthors |
| Plan a document | structure; process (outlining); house-style | words, sentences |
| Figures, tables, equations | figures-tables-equations; house-style | the rest |
| Reviews, responses, coauthors | review-and-coauthors; revision | the rest |

| When you are working on | Read |
|---|---|
| Starting, keeping momentum, outlining habits, fear, writing in English as an additional language | `references/process.md` |
| The story, IMRaD parts, titles, abstracts, introductions, methods, results, discussions, proposals, reports, theses, chapters, headings, emphasis | `references/structure.md` |
| Paragraph unity, topic sentences, sentence-to-sentence links, paragraph length, lists in prose | `references/paragraphs.md` |
| Sentence length, word order, voice, tense, first person, pronouns, parallel form, punctuation, grammar as convention, the usage watchlist | `references/sentences.md` |
| Clutter, hedges, intensifiers, nominalizations, concrete words, jargon, abbreviations, numbers in text | `references/words.md` |
| Self-revision rounds, reader simulation, cutting, reading aloud, proofreading | `references/revision.md` |
| Tables, figures, captions, legends, pointing at graphics, equations | `references/figures-tables-equations.md` |
| Friendly and formal review, responses to reviewers, writing a review, coauthors | `references/review-and-coauthors.md` |
| The author's standing preferences and voice | `references/house-style.md` |
| The four books, what each contributes, dated material, the rulings with reasons | `references/sources.md` |

## Twelve questions before anything leaves your hands

1. Can I state the question and the answer in two sentences? (Heard)
2. Does the first sentence orient the reader and take a step, and does the reader learn soon
   why the piece exists? (Alley, Zinsser)
3. Does every paragraph make one point, announced near its start? (Strunk, Heard)
4. Does each sentence begin in a way that connects it to the one before? (Alley)
5. Is the actor next to the action, the verb early, the new information at the end? (Heard,
   Strunk)
6. Is every passive doing one of its three jobs? (Heard)
7. Does every hedge match the evidence, and does any word inflate? (Heard, Alley)
8. Does every "this" point at a noun? (Alley)
9. Which words could go without loss? (Strunk, Zinsser)
10. Are every number, claim, citation, and term exactly as the source has them?
11. Does the ending add scope, consequence, or significance, or does it recap? (Zinsser,
    Heard)
12. Have I read it as a stranger, and aloud? (Heard, Alley, Zinsser)
