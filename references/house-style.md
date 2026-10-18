# House style: the author's standing preferences

This file is the layer between the author's live instructions and the four books. It
records what the author of the text wants done the same way every time: how edits are
delivered, what a section must do, how claims are bounded, which names and words stay.
Where a book rule and a house rule conflict (Zinsser's free use of dashes, Strunk's blanket
ban on "very"), the house rule wins. Where the author's own finished text breaks a book rule
on purpose (an argument-turn phrase written out, a plain emphasis word), keep it.

The rules below are a starter set, learned in live revision sessions on one author's
journal papers and book chapters. Edit this file freely: delete a rule you do not hold, add
your own, and give each rule its reason where you can, because the skill applies a rule
better when it knows what the rule protects. Keep project-specific vocabulary in the
project's own files, not here.

Precedence: the author's live instruction > the project's own conventions (style sheet,
term list, venue rules) > this file > the four books.

## What belongs here

Record a preference here when it applies to every document you write and the books do not
settle it: the delivery format you paste from, your spelling variant, your number style,
your punctuation habits (serial comma, dashes), the words you never use, the words you use
on purpose, how your finished text may be edited, and the rules your field's readers expect.

Leave out anything that belongs to one project: a term list, a chapter plan, a venue's
limits. Point the skill at those files from the project instead.

## Delivery

- Paste-ready means plain text, one physical line per paragraph, no Markdown markers,
  bullets, numbering, code fences, or hard line breaks. The interface wraps it; the author
  pastes it into a word processor.
- Every paste-ready replacement names its landing point: quote the first and last words to
  remove and say whether it replaces a sentence, a paragraph, or a subsection. Text without
  a placement anchor is incomplete.
- No em dash anywhere in manuscript prose or paste-ready text, not even one. Recast with
  commas, parentheses, a colon, a semicolon, or a full stop.
- Match the scale of an edit to the request. For a fix of a named fault, or on a chapter
  the author has finished, revise the exact phrase or sentence and preserve the paragraph's
  structure, movement, and voice. For a request to strengthen or improve a passage, propose
  the structural moves that help (a deletion of prose without value, a sentence moved to
  where its consequence follows, a buried finding brought forward), each as its own
  reversible item with the sentence quoted and a landing anchor; the author accepts or
  refuses each in one step. In every case, delete prose without value first, including a
  whole unnecessary paragraph; then repair real gaps in support, reasoning, referents, and
  narrative. Never rewrite a whole paragraph merely for style. A cut is never a substitute
  for developing a section.
- Judge every addition against the surrounding paragraph sequence, the chapter argument,
  and what the author has already removed from the chapter. A correct paragraph is still
  wrong if it repeats work already done, interrupts the subsection's job, or answers a
  question the prose has not raised. When the local argument is complete, delete rather
  than manufacture a replacement.
- Run the skill in full on every edit to manuscript prose, however small: the Revise
  rounds, the reader simulation, the signals script on the final text, and the change list.
  Loading the skill and then writing from habit does not count.

## Document and section architecture

- A subsection exists only if it answers a reader question the chapter does not already
  answer. Run that test before drafting.
- A section or subsection is never one paragraph. A heading that governs a single paragraph
  is a structural defect: fold the paragraph into the neighboring section with a lead
  sentence that ties it in, or develop the section until it answers a reader question of
  its own. A parent section's lead-in paragraph before its first subsection is not a
  section. Never keep a heading on the ground that readers will look the topic up by name;
  a lookup target is an index entry.
- Introduce every example before using it. An example enters once, at its first use in the
  chapter, with "for example" or "consider", in a sentence that presents the case itself:
  the system, its variables, the unit of observation, the sampling interval, the span. Later
  uses refer back to it under one name. A definite reference to a case the chapter has not
  presented ("In the city's annual history…") is a cold reference, the same defect as an
  undefined term, even when an earlier chapter introduced the case.
- Write the science, not the software or the filing. State what a quantity is, what
  operation produced it, what it licenses, and where it stops. Never narrate the program's
  housekeeping: files, tables, columns, rows of a data structure, dictionaries, flags, or
  artifacts the project never produced. Where an implementation detail carries a scientific
  consequence, state the consequence and drop the mechanism; where it carries none, cut the
  sentence.
- Every subsection opens with one orienting lead sentence that signals the move. Never open
  mid-thought, and never open by re-narrating prior sections.
- No deictic opener across a heading ("This is the trace…"). Re-establish the subject by
  name at every section boundary.
- Write a chapter abstract as an argument précis: the scientific problem, the design logic
  that answers it, the decisive evidence, what that evidence establishes, and the
  evidence-specific boundary. Not a method-and-results ledger, and never a closing sentence
  such as "the results apply only to the data examined."
- Write scientific prose as a connected movement: practical motive, design choice, observed
  pattern, system meaning, scientific use. Code chronology, validation receipts, procedural
  rule lists, and generic disclaimers cannot form the spine.
- Every results subsection and every substantive table or figure completes the
  evidence-to-meaning arc in local prose: report the finding, say what it establishes for
  the question, state the boundary. A caption, a tally, or a late summary cannot carry this
  work.
- Treat a request for more discussion as a diagnosis of the argument, not as a place for
  new prose. Put each result's meaning beside its evidence; use the late synthesis only for
  a chapter-level resolution.
- Reiterate a decisive distinction only at a genuine interpretive hinge, where the later
  statement adds a consequence, a use, or a boundary the first did not carry.
- Close a chapter as a conclusion: the definition with its scope, what changed in a model's
  claim, the limits, the consequence.

## Floats and equations

- Announce every table or figure by name in the prose before it appears, and claim its
  pattern by name where the reading lives. A caption is never a reference, and a later
  stray back-reference is not an introduction. Number figures by first appearance.
- Discuss a multipart figure in its displayed panel order, but keep the prose claim-led:
  begin each paragraph with the scientific claim and cite the panel in parentheses. Avoid
  "Panel (a) shows" walkthroughs.
- Do not end a caption with a generic warning that panels differ in units when the axes
  already say so.
- Introduce an equation with one plain sentence that names the operation and its object.
  Place the equation next. Define its symbols in reading order, using the same symbols in
  the prose. Never make the reader cross a method inventory before seeing the mathematical
  object.
- Every constant in a displayed formula has a stated provenance: an authentic citation
  where the literature supplies one, or an explicitly owned declaration. A constant with
  neither reads as arbitrary; a decorative citation is worse than none.
- Spell out an opaque quantity with its exact formula and one concrete numerical
  interpretation, then its full reduction ladder from elementary observation to reported
  result. A friendly paraphrase cannot replace a missing formula.
- Explain a compact statistical operation once, as a short causal sequence: what is
  resampled or compared, what stays paired, what is recalculated, how the bound is
  obtained. Remove the compressed duplicate.

## Claims, evidence, and boundaries

- Justify every scientific statement with evidence, derivation, or a reasoned connection to
  stated premises. Explain why a choice serves the task; an operation label or a limitation
  is not a justification. Flag missing support; never invent it.
- A design restriction needs a scientific rationale: why the chosen design preserves the
  intended meaning and why a live alternative would change or confound it. Parsimony or
  convenience is not a rationale.
- Use certainty for designed behavior; hedge only what the analysis genuinely declines to
  resolve. A hedge on designed behavior reads as error-framing.
- Keep a boundary only when it names the exact condition, horizon, system, or use that
  changes the interpretation. Generic epistemic modesty ("this result is bounded and
  conditional") is self-evident and weakens the contribution.
- No disclaiming tail on a definition or reading ("and it means nothing more", "it does not
  claim X") when the text never claims X. Keep the positive statement and attach, in a
  "without" clause, only the two or three misreadings a reader would plausibly make.
- True but useless prose never enters. Every sentence serves the document's live purpose.
  Delete draft rebuttals, private correction residue, settled repetition, and caveats that
  change no claim, use, scope, or decision.
- Compare summaries only when they share an observation unit and reduction ladder. Label
  each aggregation. Never compute a gain or ratio from unlike summaries.

## Names and references

- Introduce each object once, under one name, and hold that name. One object, one name,
  document-wide. Never rotate names for variety.
- A definite article only on an object already introduced.
- No unresolved reference. "Both designs", "these cells", "the former case", and a bare
  demonstrative must name their members or point unmistakably to them in the same or the
  immediately preceding sentence. Verify the referent; never guess.
- State a comparison in words at first statement: what two things are compared, on which
  quantity, and what passing means.
- Name each object in its own sentence. Compressed double naming that elides the verb ("We
  call X the A, and Y the B") reads as garbled.
- No provenance tag on every mention. A qualifier that records how or when an object was
  chosen ("declared", "registered", "prespecified") appears only where that fact is the
  sentence's claim, written with its timing ("declared before fitting"); the object's name
  carries every other mention. Delete the tag rather than rotating to a synonym; a defined
  term that contains the word stays.
- Keep "reader" for the human audience. A parser, model, or algorithm keeps its technical
  name.
- Never carry code language, pipeline terms, file names, or planning vocabulary into prose,
  and never preserve such a term by defining it for the reader. Translate every internal
  term through operation, measured quantity, scientific question, meaning, and boundary.
- Name a plain fact directly, with its number: "the history contains only 13
  observations," never "row scarcity."
- Do not name a diagnostic with evaluative shorthand ("worth", "utility"); name the
  measured quantity and its scope ("short-horizon error reduction").
- State a relationship with a precise verb, never with a vague one such as "belong to".

## Sentences and words

- Literal over figurative. No decorative metaphor, personification, or flourish in place of
  a precise statement: "a parameter worth varying", not "a dial worth turning". Never swap
  one flourish for another. Established technical terms and exact quotations stay, whatever
  their figurative origin.
- A count is followed by first, second, third. An enumeration paragraph that opens "First,"
  needs a bridge sentence at the end of the immediately preceding paragraph, with the
  author as actor: "Five principles carry that separation through the method. We state them
  here and develop each in its own section."
- Use measured first-person plural ("we") when guiding a choice, comparison, or
  interpretation. The subject names the actor and the verb names the action. Never use "we"
  to narrate drafting or promise later content.
- Lead with the finding; subordinate the apparatus. No procedure-first openers.
- Keep an example only when it establishes an inference the general sentence lacks, such as
  arithmetic the reader must verify. Otherwise write the general sentence.
- Read the chapter's context before adding any example or concrete instance. A principles or
  theory narrative carries no worked example, and an example the author has removed from a
  chapter is never reintroduced by a later insertion, however apt it looks in the sentence at
  hand. Before drafting, check whether the chapter carries the example elsewhere, whether
  the author has cut it, and whether the section's register is theoretical.
- Numbers that take part in an arithmetic the prose states appear as numerals so the reader
  can verify the chain at sight; purely descriptive small counts stay as words.
- Describe a recursion or accumulation once, from the reader's position: what the equation
  reads at the next step and what each part contributes. Not a run of "it weights… it
  weights…" fragments.
- Keep the stable grammatical roles of an event and its recipient. Once an event is defined
  as occurring for an object, the event stays the subject.
- Sentence length follows the chain of reasoning, not a word count.

## The author's voice (fill this in)

Record here what an editor must leave alone in your own text. The skill reads this section
before it touches a finished chapter, and the rules in words.md and sentences.md yield to
it. Replace the examples with your own.

- Argument turns you write out on purpose are not filler ("However, that does not mean that
  the model is wrong. Quite on the contrary"; "It is also important to note that"). An
  editor does not strip them as machine tells. List yours.
- Plain emphasis words you use deliberately ("very important", "crystal clear"): they stay
  when your text is edited and appear sparingly when text is drafted for you. List yours.
- Your punctuation habits for asides (spaced en dashes, parentheses, commas) and anything
  else that marks a sentence as yours.
- On a chapter you have finished, the editor reports only factual or scientific errors and
  does not polish.
