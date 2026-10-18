#!/usr/bin/env python3
"""Mechanical prose-signal scanner for scientific writing.

Reports regex/word-list heuristics (sentence length, passive-voice
candidates, clutter phrases, hedges, nominalizations, acronyms, echoes,
and more) on plain-text, Markdown, or .docx input. It never judges prose;
it counts things and shows examples so a human editor can decide.

Limits: sentence splitting is a stdlib regex with abbreviation/decimal/
initials guards, not a parser; every "heuristic" section can misfire on
unusual phrasing. Citations in parentheses are left in place and count
toward word totals.

Usage:
    python3 prose_signals.py file.txt [file2.md ...] [--json] [--top N] [--quiet]
    cat file.txt | python3 prose_signals.py

Standard library only. No network. Exit code is always 0.
"""
from __future__ import annotations

import argparse
import collections
import copy
import json
import re
import statistics
import sys
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple, Union

# ---------------------------------------------------------------------------
# Data blocks. Keep phrase/word lists here so an editor can extend them
# without touching any function body. One block per source, labeled.
# ---------------------------------------------------------------------------

# STRUNK_CLUTTER -- Strunk, The Elements of Style (1918/1920), rule 13
# ("Omit needless words") and chapter V word/phrase notes. Most entries are
# matched as literal, case-insensitive phrases. A few are regex templates
# (they contain \, (, ), or |) and are auto-detected and used as regex.
STRUNK_CLUTTER: List[str] = [
    "the fact that",
    "owing to the fact that",
    "in spite of the fact that",
    "call your attention to the fact that",
    "the question as to whether",
    "as to whether",
    "there is no doubt but that",
    "no doubt but that",
    r"for \w+ purposes",
    "he is a man who",
    "in a hasty manner",
    r"in a \w+ manner",
    "this is a subject which",
    "in many cases",
    "in most cases",
    "in the case of",
    "it has rarely been the case",
    r"of a \w+ character",
    r"of a \w+ nature",
    "along these lines",
    "along the lines of",
    "one of the most",
    "student body",
    r"the reason (?:that|why) .{1,60} (?:is|was) that",
    "as good or better than",
    "different than",
    "respectively",
    "worth while",
    "kind of",
    "sort of",
    "in connection with",
    "it is interesting to",
    "an interesting",
    "a factor in",
    "feature of",
    "system of",
    "possess",
    "the possessor of",
]

# GENERAL_CLUTTER -- general, not from a specific book. Widely taught
# redundancies and filler phrases common in scientific/technical prose.
GENERAL_CLUTTER: List[str] = [
    "in order to",
    "due to the fact that",
    "at this point in time",
    "at the present time",
    "a number of",
    "the majority of",
    "in the event that",
    "prior to",
    "subsequent to",
    "utilize",
    "utilization",
    "in the process of",
    "with regard to",
    "with respect to",
    "in terms of",
    "for the purpose of",
    "has the ability to",
    "is able to",
    "are able to",
    "it should be noted that",
    "it is important to note that",
    "it is worth noting that",
    "needless to say",
    "as a matter of fact",
    "in close proximity",
    "basically",
    "essentially",
    "actually",
    "currently",
    "in the field of",
    "the process of",
    "serves to",
    "it can be seen that",
    "it is clear that",
    "it is evident that",
    "in a very real sense",
    "on a daily basis",
    "take into consideration",
    "make a decision",
    "conduct an investigation",
    "perform an analysis",
    "carry out an analysis",
    "make an assessment",
    "provide an explanation",
    "give consideration to",
    "reach a conclusion",
]

# ZINSSER_CLUTTER -- phrases from Zinsser, On Writing Well, chapters 3, 10,
# and 16. Each entry is a bare phrase/regex string (no suggested
# replacement) or a (phrase_or_regex, replacement) pair. Regex vs. literal
# is auto-detected the same way as STRUNK_CLUTTER above.
ZINSSER_CLUTTER: List[Union[str, Tuple[str, str]]] = [
    # Long words
    ("assistance", "help"),
    ("numerous", "many"),
    ("facilitate", "ease"),
    ("remainder", "rest"),
    ("initial", "first"),
    ("implement", "do"),
    ("sufficient", "enough"),
    ("attempt", "try"),
    ("referred to as", "called"),
    # Fad words and verbs
    "paradigm",
    ("prioritize", "rank"),
    "potentialize",
    (r"\bdialogu(e|ed|ing) with\b", "talk to"),
    ("interface with", "work with"),
    # Clusters that announce
    "I might add",
    "it should be pointed out",
    "it is interesting to note",
    # Inflations
    ("with the possible exception of", "except"),
    ("due to the fact that", "because"),
    ("totally lacked the ability to", "could not"),
    ("until such time as", "until"),
    ("for the purpose of", "for"),
    # Clutter and euphemism
    (r"\bexperienc(e|es|ed|ing)\b", "plain verb"),
    ("at the present time", "now"),
    ("presently", "now"),
    ("currently", "(often delete)"),
    ("personal friend", "friend"),
    ("head up", "head"),
    ("face up to", "face"),
    ("free up", "free"),
    ("order up", "order"),
    # Little qualifiers
    "a bit",
    "a little",
    "sort of",
    "kind of",
    "rather",
    "quite",
    "pretty much",
    "in a sense",
    r"\btoo (large|small|high|low|many|few|much|little)\b",
    # Adverbs that measure nothing
    "decidedly",
    "eminently",
    "arguably",
    "virtually",
    # Value placed before the fact
    "surprisingly",
    "predictably",
    "of course",
    "interestingly",
]

# ALLEY_WATCHLIST -- terms from Michael Alley, The Craft of Scientific
# Writing, Lessons 2, 4, and 9. Same entry style as ZINSSER_CLUTTER above.
ALLEY_WATCHLIST: List[Union[str, Tuple[str, str]]] = [
    # Pretentious words
    ("approximately", "about"),
    ("component", "part"),
    ("facilitate", "help"),
    r"\b\w+ability\b",
    ("utilization", "use"),
    ("utilize", "use"),
    ("elucidate", "reveal"),
    ("prioritize", "rank"),
    # Arrogant phrases
    "as is well known",
    "of course",
    r"\bclearly (demonstrat|show|indicat|establish)\w*\b",
    "unambiguous",
    "unambiguously",
    "it is obvious",
    "obviously",
    # Exaggeration and self-praise
    "countless",
    r"\b(our|a|the) thorough\b",
    r"\bprov(e|es|ed|ing)\b",
    r"\boptim(al|um)\b",
    "very unique",
    "most critical",
    "most unique",
    # Abstract nouns to anchor -- low confidence: legitimate when the
    # reader already holds the concept (flagged via LOW_CONFIDENCE_CLUTTER).
    "ability",
    "approach",
    "capability",
    "concept",
    "environment",
    "factor",
    "nature",
    "parameter",
    # Redundancies
    "already existing",
    "alternative choices",
    "basic fundamentals",
    "completely eliminate",
    "continue to remain",
    "currently being",
    "currently underway",
    "empty space",
    "had done previously",
    "introduced a new",
    "mix together",
    "never before",
    "none at all",
    "now at this time",
    "period of time",
    "private industry",
    "separate entities",
    "start out",
    "still persists",
    # Writing zeroes
    "as a matter of fact",
    "I might add that",
    "it is noteworthy that",
    "it is significant that",
    "it should be pointed out that",
    "the course of",
    "the fact that",
    "the presence of",
    # Phrase reductions
    ("at this point in time", "now"),
    ("at that point in time", "then"),
    ("due to the fact that", "because"),
    ("has the ability to", "can"),
    ("has the potential to", "can"),
    ("in the event that", "if"),
    ("in the vicinity of", "near"),
    ("owing to the fact that", "because"),
    # Weak verb phrases
    ("made the arrangement for", "arranged"),
    ("made the decision", "decided"),
    ("made the measurement of", "measured"),
    ("performed the development of", "developed"),
    ("is dependent on", "depends on"),
    ("is a result from", "results from"),
    ("is used to detect", "detects"),
    (r"\bmak(e|es|ing) (a|the) measurement\b", "measure"),
    # Informal in formal papers. "vs." and "&" use a regex (rather than the
    # literal path) because a trailing "." or a bare "&" defeats a plain
    # \b...\b word-boundary match.
    ("a lot", "much or many"),
    (r"\bg(et|ets|ot|otten) (a|the|an)\b", "obtain"),
    (r"\bvs\.(?!\w)", "versus"),
    (r"\&", "and"),
    (r"\b\w+n't\b|\b(it|that|there|he|she|we|they|you|I)'(s|re|ve|ll|d|m)\b", "write out"),
    # Intensifier
    ("very", "cut; use a stronger word"),
]

# HEARD_WATCHLIST -- guidance from Stephen Heard, The Scientist's Guide to
# Writing, chapters 19 and 20. Same entry style as ZINSSER_CLUTTER above.
HEARD_WATCHLIST: List[Union[str, Tuple[str, str]]] = [
    # Roundabout phrases
    ("owing to the fact that", "because"),
    ("notwithstanding the fact that", "although"),
    ("is able to", "can"),
    ("are able to", "can"),
    ("the majority of", "most"),
    ("endeavor", "try"),
    ("terminate", "end"),
    # Tautologous modifiers
    "completely finish",
    "may potentially",
    "ultimate result",
    r"\b(blue|red|green|yellow|white|black) in colou?r\b",
    # Empty modifiers
    "really",
    "basically",
    "actually",
    "indeed",
    "quite",
    "various",
    # Padding
    "the fact of the matter is",
    "in our opinion",
    "needless to say",
    "it obviously follows that",
    "for all intents and purposes",
    # Metadiscourse
    ("we believe that our results establish", "state the result"),
    ("in this study we", "we"),
    ("the objective of this study was to", "we sought to"),
    ("it is important to keep in mind that", "cut"),
    # Nominalizations to unwind
    ("conducted an analysis", "analyzed"),
    ("conduct an analysis", "analyze"),
    ("provided a review of", "reviewed"),
    ("had superior performance", "performed better"),
    ("our intention is to", "we intend to"),
]

# HEDGES -- hedging words and phrases. Legitimate when the science is
# genuinely uncertain; the signal worth flagging is stacking and habit.
HEDGES: List[str] = [
    "may", "might", "could", "possibly", "perhaps", "it seems", "seems to",
    "appears to", "appear to", "suggests that", "suggest that", "somewhat",
    "relatively", "fairly", "to some extent", "arguably", "seemingly",
    "likely", "potentially", "tend to", "tends to", "in some sense",
    "more or less",
]

# INTENSIFIERS -- intensifiers and empty modifiers. "so " before a small
# set of adjectives is implemented as a regex template.
INTENSIFIERS: List[str] = [
    "very", "quite", "rather", "extremely", "highly", "really", "truly",
    "certainly", "clearly", "obviously", "of course", "significantly",
    "dramatically", "remarkably", "interestingly", "importantly", "notably",
    "literally", "absolutely", "completely", "totally",
    r"\bso (?:good|large|small|high|low|strong|weak|important|much|many)\b",
    "critically", "crucially", "vitally",
]

# PASSIVE_IRREGULAR_PARTICIPLES -- past participles that a generic -ed/-en
# suffix check would miss, used by the passive-voice heuristic.
PASSIVE_IRREGULAR_PARTICIPLES: List[str] = [
    "shown", "seen", "given", "taken", "known", "found", "made", "done",
    "built", "held", "kept", "left", "met", "put", "set", "run", "begun",
    "chosen", "driven", "drawn", "grown", "thrown", "written", "understood",
    "brought", "thought", "sought", "taught", "caught", "bought", "fought",
    "sold", "told", "led", "fed", "read", "said", "paid", "laid", "felt",
    "dealt", "meant", "sent", "spent", "lent", "lost", "cut", "hit", "let",
    "split", "spread", "shut",
]

# STOPWORDS -- articles, prepositions, conjunctions, pronouns, auxiliaries,
# and common adverbs. Used by the noun-string and echo heuristics.
STOPWORDS = {
    "a", "an", "the",
    "and", "or", "but", "nor", "so", "yet", "for",
    "in", "on", "at", "by", "to", "of", "with", "from", "into", "onto",
    "over", "under", "about", "above", "below", "between", "among",
    "through", "during", "before", "after", "across", "against", "along",
    "around", "behind", "beside", "besides", "beyond", "despite", "except",
    "inside", "near", "outside", "since", "toward", "towards", "upon",
    "within", "without", "per", "via", "as", "than", "then",
    "i", "me", "my", "mine", "we", "us", "our", "ours", "you", "your",
    "yours", "he", "him", "his", "she", "her", "hers", "it", "its", "they",
    "them", "their", "theirs", "this", "that", "these", "those", "who",
    "whom", "whose", "which", "what", "whoever", "whatever", "whichever",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "can", "could", "shall", "should", "will", "would", "may", "might",
    "must", "not", "no",
    "too", "also", "just", "only", "even", "still", "already", "again",
    "here", "there", "now", "then", "always", "often", "sometimes", "never",
    "up", "down", "out", "off", "further", "once",
    "each", "few", "more", "most", "other", "some", "such", "own", "same",
    "if", "because", "while", "although", "though", "unless", "until",
    "whereas", "both", "either", "neither", "all", "any", "every",
}

# Small allowlist of common words that end in a nominalization suffix but
# are not meaningfully "nominalizations" in the sense this heuristic targets.
NOMINALIZATION_ALLOWLIST = {
    "nation", "station", "moment", "element", "comment", "document",
    "equipment", "environment", "instrument", "government", "city",
    "quantity", "entity", "density", "velocity", "ability", "probability",
    "business", "witness", "illness",
}

# Common all-caps tokens excluded from the acronym scan.
ACRONYM_EXCLUSIONS = {
    "US", "UK", "OK", "AND", "THE",
    "ASCII", "PDF", "HTML", "URL", "USA", "FOR", "NOT", "BUT", "ALL", "ANY",
    "NEW", "END", "START", "NOTE", "TODO", "EOF", "DOI", "ISBN",
}

# Clutter entries reported as low-confidence (common technical or generic
# usage overlaps with the flagged phrase or pattern).
LOW_CONFIDENCE_CLUTTER = {
    "system of",
    r"\b\w+ability\b",
    r"\bg(et|ets|ot|otten) (a|the|an)\b",
    "ability", "approach", "capability", "concept", "environment",
    "factor", "nature", "parameter",
}

# ---------------------------------------------------------------------------
# Sentence-splitting support: abbreviations, decimals, initials.
# ---------------------------------------------------------------------------

_ABBREVIATIONS = [
    "e.g.", "i.e.", "et al.", "Fig.", "Figs.", "Eq.", "Eqs.", "Dr.", "Mr.",
    "Ms.", "vs.", "cf.", "approx.", "No.", "ca.", "Ref.", "Refs.", "Table",
    "Sect.",
]
_ABBREV_PATTERNS = [re.compile(re.escape(a), re.IGNORECASE) for a in _ABBREVIATIONS]
_DECIMAL_RE = re.compile(r"(?<=\d)\.(?=\d)")
_INITIAL_RUN_RE = re.compile(r"\b([A-Z])\.(?=\s+[A-Z]\.)")
_SENTINEL = "\x00"


def _protect_periods(paragraph: str) -> str:
    """Replace periods that should not end a sentence with a sentinel."""
    protected = paragraph
    for pattern in _ABBREV_PATTERNS:
        protected = pattern.sub(lambda m: m.group(0).replace(".", _SENTINEL), protected)
    protected = _DECIMAL_RE.sub(_SENTINEL, protected)
    # Two passes catch short chains of initials ("J. R. Smith").
    protected = _INITIAL_RUN_RE.sub(lambda m: m.group(1) + _SENTINEL, protected)
    protected = _INITIAL_RUN_RE.sub(lambda m: m.group(1) + _SENTINEL, protected)
    return protected


_SENTENCE_BOUNDARY_RE = re.compile(r'(?<=[.?!])\s+(?=[A-Z0-9"‘’“”\'])')
_HEADING_RE = re.compile(r"^#{1,6}\s+\S")
_FENCE_RE = re.compile(r"(?ms)^```.*?^```\s*$")
_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")


def load_text(paths: List[str]) -> str:
    """Read input text: stdin if no paths, else each path (.docx via zipfile/XML)."""
    if not paths:
        return sys.stdin.read()
    chunks = []
    for path in paths:
        if path.lower().endswith(".docx"):
            chunks.append(_load_docx(path))
        else:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                chunks.append(f.read())
    return "\n\n".join(chunks)


def _load_docx(path: str) -> str:
    """Extract paragraph text from word/document.xml, joining runs per w:p."""
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as f:
            root = ET.fromstring(f.read())
    paragraphs = []
    for p in root.iter(ns + "p"):
        text = "".join(t.text or "" for t in p.iter(ns + "t"))
        paragraphs.append(text)
    return "\n\n".join(paragraphs)


def split_paragraphs(text: str) -> List[str]:
    """Split on blank lines. Markdown headings become their own paragraph;
    fenced code blocks are dropped."""
    text = _FENCE_RE.sub("", text)
    blocks = re.split(r"\n\s*\n+", text.strip())
    paragraphs: List[str] = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        buffer: List[str] = []
        for line in block.split("\n"):
            stripped = line.strip()
            if _HEADING_RE.match(stripped):
                if buffer:
                    joined = " ".join(x for x in buffer if x)
                    if joined:
                        paragraphs.append(joined)
                    buffer = []
                paragraphs.append(stripped)
            else:
                buffer.append(stripped)
        if buffer:
            joined = " ".join(x for x in buffer if x)
            if joined:
                paragraphs.append(joined)
    return paragraphs


def split_sentences(paragraph: str) -> List[str]:
    """Split a paragraph into sentences on . ? ! + whitespace + capital/digit/
    quote, with guards for common abbreviations, decimals, and initials."""
    if not paragraph or not paragraph.strip():
        return []
    protected = _protect_periods(paragraph)
    parts = _SENTENCE_BOUNDARY_RE.split(protected)
    sentences = []
    for part in parts:
        restored = part.replace(_SENTINEL, ".").strip()
        if restored:
            sentences.append(restored)
    return sentences


def tokenize(text: str) -> List[str]:
    """Whitespace tokens with surrounding punctuation stripped; hyphenated
    and apostrophe-joined words stay one token."""
    return _WORD_RE.findall(text)


# ---------------------------------------------------------------------------
# Sentence records: build once, reuse across analyzers (avoids quadratic
# re-scanning of sentences).
# ---------------------------------------------------------------------------

Sentence = Dict[str, object]  # keys: text (str), para (int), words (int), tokens (List[str])


def _build_sentences(paragraphs: List[str]) -> List[Sentence]:
    sentences: List[Sentence] = []
    for p_idx, para in enumerate(paragraphs, start=1):
        for sent_text in split_sentences(para):
            tokens = tokenize(sent_text)
            sentences.append({"text": sent_text, "para": p_idx, "words": len(tokens), "tokens": tokens})
    return sentences


# ---------------------------------------------------------------------------
# Compiled regex used by several analyzers.
# ---------------------------------------------------------------------------

_REGEXY_RE = re.compile(r"[\\|(){}]")


def _compile_pattern(phrase: str) -> "re.Pattern":
    """Auto-detect a regex template (contains \\, (, ), or |) vs. a literal
    phrase (wrapped in word boundaries, case-insensitive)."""
    if _REGEXY_RE.search(phrase):
        return re.compile(phrase, re.IGNORECASE)
    return re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)


# Clutter sources, in report order. Labels are the plain words used to name
# a hit's source block; "general" stays lowercase to match the label used
# throughout the report.
_CLUTTER_SOURCES: List[Tuple[str, List[Union[str, Tuple[str, str]]]]] = [
    ("Strunk", STRUNK_CLUTTER),
    ("general", GENERAL_CLUTTER),
    ("Zinsser", ZINSSER_CLUTTER),
    ("Alley", ALLEY_WATCHLIST),
    ("Heard", HEARD_WATCHLIST),
]


def _clutter_entry_pattern_and_replacement(entry: Union[str, Tuple[str, str]]) -> Tuple[str, Optional[str]]:
    """An entry is a bare phrase/regex string, or a (phrase_or_regex,
    replacement) pair. Normalize both to (pattern_text, replacement)."""
    if isinstance(entry, tuple):
        return entry[0], entry[1]
    return entry, None


def _format_replacement(replacements: List[Tuple[str, str]]) -> Optional[str]:
    """Collapse a phrase's (source, replacement) pairs to display text.
    Most phrases carry one suggestion; a few sources disagree (e.g.
    "facilitate" -> "ease" per Zinsser, "help" per Alley), so distinct
    suggestions are kept and labeled by source rather than silently
    dropped."""
    if not replacements:
        return None
    distinct: List[Tuple[str, str]] = []
    seen_text = set()
    for source, repl in replacements:
        if repl not in seen_text:
            distinct.append((source, repl))
            seen_text.add(repl)
    if len(distinct) == 1:
        return distinct[0][1]
    return "; ".join(f"{repl} ({source})" for source, repl in distinct)


def _build_clutter_index() -> List[dict]:
    """Merge all five clutter blocks into one list of unique patterns. A
    phrase repeated across blocks (e.g. "the fact that" in both Strunk and
    Alley) is merged into a single entry that lists every source, so a hit
    is reported once rather than once per source."""
    by_pattern: "collections.OrderedDict[str, dict]" = collections.OrderedDict()
    for source_label, block in _CLUTTER_SOURCES:
        for entry in block:
            pattern_text, replacement = _clutter_entry_pattern_and_replacement(entry)
            rec = by_pattern.get(pattern_text)
            if rec is None:
                rec = {
                    "pattern_text": pattern_text,
                    "compiled": _compile_pattern(pattern_text),
                    "sources": [],
                    "replacements": [],
                    "low_confidence": False,
                }
                by_pattern[pattern_text] = rec
            rec["sources"].append(source_label)
            if replacement:
                rec["replacements"].append((source_label, replacement))
            if pattern_text in LOW_CONFIDENCE_CLUTTER:
                rec["low_confidence"] = True
    return list(by_pattern.values())


_CLUTTER_INDEX: List[dict] = _build_clutter_index()
_HEDGE_PATTERNS: List[Tuple[str, "re.Pattern"]] = [(p, _compile_pattern(p)) for p in HEDGES]
_INTENSIFIER_PATTERNS: List[Tuple[str, "re.Pattern"]] = [(p, _compile_pattern(p)) for p in INTENSIFIERS]

_BE_FORMS = r"(?:am|is|are|was|were|be|been|being)"
_PARTICIPLE = r"(?:[A-Za-z]+(?:ed|en)|" + "|".join(PASSIVE_IRREGULAR_PARTICIPLES) + r")"
_PASSIVE_RE = re.compile(r"\b" + _BE_FORMS + r"\b(?:\s+\w+ly)?\s+\b" + _PARTICIPLE + r"\b", re.IGNORECASE)

_EXPLETIVE_THERE_RE = re.compile(r"^\s*There\s+(?:is|are|was|were|has been|have been)\b", re.IGNORECASE)
_EXPLETIVE_IT_RE = re.compile(r"^\s*It\s+(?:is|was)\s+\w+\s+(?:that|which)\b", re.IGNORECASE)

_NOMINALIZATION_SUFFIXES = ("tion", "sion", "ment", "ance", "ence", "ity", "ness", "ism")

_VAGUE_PRONOUNS = {"this", "these", "that", "those", "it", "which", "such"}
_VAGUE_VERB_WORDS = {
    "is", "are", "was", "were", "has", "have", "had", "can", "could", "may",
    "might", "will", "would", "should", "does", "do", "did", "means",
    "suggests", "shows", "indicates", "implies", "reflects", "demonstrates",
    "raises", "leaves", "makes", "allows", "requires", "involves",
    "includes", "follows",
}

_ACRONYM_RE = re.compile(r"\b[A-Z]{2,6}[0-9]*\b")
_ROMAN_NUMERAL_RE = re.compile(r"^[IVXLCDM]+$")


def _looks_verb_like(word: str) -> bool:
    w = word.lower()
    if w in _VAGUE_VERB_WORDS:
        return True
    return w.endswith("s") or w.endswith("ed")


def _is_nominalization(word: str) -> bool:
    w = word.lower()
    if len(w) < 7 or w in NOMINALIZATION_ALLOWLIST:
        return False
    return w.endswith(_NOMINALIZATION_SUFFIXES)


# ---------------------------------------------------------------------------
# Analyzers. Each returns a plain dict. None issues a verdict; each carries
# a one-line note on what the heuristic misses.
# ---------------------------------------------------------------------------

def analyze_long_sentences(sentences: List[Sentence]) -> dict:
    ranked = sorted(sentences, key=lambda s: -s["words"])
    return {
        "note": "Sorted longest first. Length alone is not a defect; it compounds other problems.",
        "items": [{"text": s["text"], "words": s["words"], "para": s["para"]} for s in ranked],
    }


def analyze_paragraphs(paragraphs: List[str], sentences: List[Sentence]) -> dict:
    word_counts = [len(tokenize(p)) for p in paragraphs]
    sentence_counts = collections.Counter(s["para"] for s in sentences)
    over_200 = [i + 1 for i, wc in enumerate(word_counts) if wc > 200]
    single_sentence = [i + 1 for i in range(len(paragraphs)) if sentence_counts.get(i + 1, 0) == 1]
    return {
        "note": "Strunk: a paragraph is a unit of composition. Single-sentence paragraphs suit transitions; flag if frequent.",
        "word_counts": word_counts,
        "over_200_words": over_200,
        "single_sentence_paragraphs": single_sentence,
    }


def analyze_passive(sentences: List[Sentence]) -> dict:
    hits = [s for s in sentences if _PASSIVE_RE.search(str(s["text"]))]
    share = (len(hits) / len(sentences)) if sentences else 0.0
    return {
        "heuristic_note": (
            "Regex heuristic: a 'be' form plus a likely past participle. Misses irregular "
            "participles not in PASSIVE_IRREGULAR_PARTICIPLES and flags some adjectival uses "
            "(e.g. 'was interesting'). 'Were used' in a Methods section is often the right "
            "choice; the reader decides. Adjectival uses (was concerned, is located) also "
            "match; a Methods section can run high on passives and be right."
        ),
        "sentence_count": len(hits),
        "share_of_sentences": share,
        "examples": [{"text": h["text"], "para": h["para"]} for h in hits],
    }


def analyze_expletives(sentences: List[Sentence]) -> dict:
    hits = [
        s for s in sentences
        if _EXPLETIVE_THERE_RE.search(str(s["text"])) or _EXPLETIVE_IT_RE.search(str(s["text"]))
    ]
    return {
        "heuristic_note": "Regex heuristic keyed on sentence-initial phrasing; misses reworded or mid-sentence expletives.",
        "count": len(hits),
        "examples": [{"text": h["text"], "para": h["para"]} for h in hits],
    }


def analyze_nominalizations(all_words: List[str]) -> dict:
    counts: collections.Counter = collections.Counter()
    for w in all_words:
        if _is_nominalization(w):
            counts[w.lower()] += 1
    total_noms = sum(counts.values())
    total_words = len(all_words)
    density = (total_noms / total_words * 100) if total_words else 0.0
    return {
        "note": "Technical terms such as 'regression' or 'estimation' can be legitimate; the reader decides.",
        "total_count": total_noms,
        "density_per_100_words": density,
        "top": [{"word": w, "count": c} for w, c in counts.most_common(10)],
    }


def analyze_clutter(sentences: List[Sentence]) -> dict:
    total = 0
    phrases_found = []
    by_source: "collections.OrderedDict[str, int]" = collections.OrderedDict(
        (label, 0) for label, _ in _CLUTTER_SOURCES
    )
    for rec in _CLUTTER_INDEX:
        pattern = rec["compiled"]
        count = 0
        example = None
        for s in sentences:
            n = len(pattern.findall(str(s["text"])))
            if n:
                count += n
                if example is None:
                    example = s["text"]
        if count:
            total += count
            for source_label in rec["sources"]:
                by_source[source_label] += count
            phrases_found.append({
                "phrase": rec["pattern_text"],
                "sources": rec["sources"],
                "count": count,
                "example": example,
                "low_confidence": rec["low_confidence"],
                "replacement": _format_replacement(rec["replacements"]),
            })
    phrases_found.sort(key=lambda x: -x["count"])
    return {
        "heuristic_note": (
            "Case-insensitive phrase/regex matching against fixed lists from five sources "
            "(Strunk, general, Zinsser, Alley, Heard); a few entries (e.g. 'system of') are "
            "low-confidence and may hit legitimate technical or generic usage. A phrase "
            "listed by more than one source is still counted once, not once per source."
        ),
        "total_count": total,
        "phrases_found": phrases_found,
        "by_source": dict(by_source),
    }


def analyze_hedges(sentences: List[Sentence], total_words: int) -> dict:
    total = 0
    counts: collections.Counter = collections.Counter()
    stacked = []
    for s in sentences:
        n_in_sentence = 0
        for word, pattern in _HEDGE_PATTERNS:
            n = len(pattern.findall(str(s["text"])))
            if n:
                counts[word] += n
                total += n
                n_in_sentence += n
        if n_in_sentence >= 2:
            stacked.append(s)
    density = (total / total_words * 100) if total_words else 0.0
    return {
        "note": (
            "Hedging is often the right choice when the analysis is genuinely uncertain; "
            "the signal worth acting on is stacking and habit, not any single hedge word."
        ),
        "total_count": total,
        "density_per_100_words": density,
        "by_word": counts.most_common(),
        "stacked_sentence_count": len(stacked),
        "stacked_examples": [{"text": s["text"], "para": s["para"]} for s in stacked],
    }


def analyze_intensifiers(sentences: List[Sentence]) -> dict:
    total = 0
    counts: collections.Counter = collections.Counter()
    examples = []
    for s in sentences:
        found = False
        for word, pattern in _INTENSIFIER_PATTERNS:
            n = len(pattern.findall(str(s["text"])))
            if n:
                counts[word] += n
                total += n
                found = True
        if found:
            examples.append(s)
    return {
        "heuristic_note": "'significantly' is ambiguous outside a reported statistical test; check context before cutting it.",
        "total_count": total,
        "by_word": counts.most_common(),
        "examples": [{"text": s["text"], "para": s["para"]} for s in examples],
    }


def analyze_vague_pronouns(sentences: List[Sentence]) -> dict:
    hits = []
    for s in sentences:
        tokens = s["tokens"]
        if len(tokens) >= 2 and tokens[0].lower() in _VAGUE_PRONOUNS and _looks_verb_like(tokens[1]):
            hits.append(s)
    return {
        "note": "A bare 'This' at the start of a sentence often has an unclear referent; attach a noun (This gap, These estimates).",
        "count": len(hits),
        "examples": [{"text": h["text"], "para": h["para"]} for h in hits],
    }


def analyze_noun_strings(sentences: List[Sentence]) -> dict:
    hits = []
    for s in sentences:
        run: List[str] = []
        for tok in list(s["tokens"]) + [""]:
            low = tok.lower()
            ok = bool(tok) and low not in STOPWORDS and not low.endswith(("ly", "ed", "ing"))
            if ok:
                run.append(tok)
            else:
                if len(run) >= 4:
                    hits.append({"text": s["text"], "para": s["para"], "run": " ".join(run)})
                run = []
    return {
        "heuristic_note": "Rough heuristic: flags any run of 4+ non-stopword tokens, including legitimate technical noun phrases.",
        "count": len(hits),
        "examples": hits,
    }


def analyze_punctuation(sentences: List[Sentence]) -> dict:
    em_dash_count = 0
    em_dash_examples = []
    en_dash_count = 0
    double_hyphen_count = 0
    semicolon_count = 0
    exclamation_count = 0
    paren_count = 0
    however_initial_count = 0
    data_is_count = 0
    data_are_count = 0
    etc_count = 0
    eg_count = 0
    ie_count = 0
    total_words = 0
    for s in sentences:
        t = str(s["text"])
        total_words += int(s["words"])
        n_em = t.count("—")
        if n_em:
            em_dash_count += n_em
            em_dash_examples.append({"text": t, "para": s["para"]})
        en_dash_count += len(re.findall(r"\s–\s", t))
        double_hyphen_count += t.count("--")
        semicolon_count += t.count(";")
        exclamation_count += t.count("!")
        paren_count += t.count("(") + t.count(")")
        if re.match(r"^\s*However\b", t):
            however_initial_count += 1
        data_is_count += len(re.findall(r"\bdata\s+is\b", t, re.IGNORECASE))
        data_are_count += len(re.findall(r"\bdata\s+are\b", t, re.IGNORECASE))
        etc_count += len(re.findall(r"\betc\.", t, re.IGNORECASE))
        eg_count += len(re.findall(r"\be\.g\.", t, re.IGNORECASE))
        ie_count += len(re.findall(r"\bi\.e\.", t, re.IGNORECASE))
    n_sentences = len(sentences)
    semicolons_per_100_sentences = (semicolon_count / n_sentences * 100) if n_sentences else 0.0
    parens_per_100_words = (paren_count / total_words * 100) if total_words else 0.0
    return {
        "heuristic_note": (
            "Sentence-initial 'However': Strunk (1920) said not first; modern usage accepts it. "
            "'data is' vs. 'data are' is informational; usage varies by field."
        ),
        "em_dash_count": em_dash_count,
        "em_dash_examples": em_dash_examples,
        "en_dash_spaced_count": en_dash_count,
        "double_hyphen_count": double_hyphen_count,
        "semicolon_count": semicolon_count,
        "semicolons_per_100_sentences": semicolons_per_100_sentences,
        "exclamation_count": exclamation_count,
        "parentheses_count": paren_count,
        "parentheses_per_100_words": parens_per_100_words,
        "however_sentence_initial_count": however_initial_count,
        "data_is_count": data_is_count,
        "data_are_count": data_are_count,
        "etc_count": etc_count,
        "eg_count": eg_count,
        "ie_count": ie_count,
    }


def analyze_acronyms(sentences: List[Sentence], paragraphs: List[str]) -> dict:
    # A "heading" is a paragraph that is entirely uppercase (str.isupper()
    # ignores digits/punctuation and requires at least one cased letter).
    # A token seen only inside such lines is skipped below.
    heading_paragraphs = {
        i + 1 for i, p in enumerate(paragraphs) if p.strip() and p.strip().isupper()
    }
    first_seen: Dict[str, int] = {}
    counts: collections.Counter = collections.Counter()
    seen_outside_heading = set()
    for s in sentences:
        para_idx = int(s["para"])
        outside_heading = para_idx not in heading_paragraphs
        for m in _ACRONYM_RE.finditer(str(s["text"])):
            token = m.group(0)
            if len(token) < 2:  # single letters
                continue
            if _ROMAN_NUMERAL_RE.match(token):  # e.g. "Chapter II"
                continue
            if token in ACRONYM_EXCLUSIONS:
                continue
            counts[token] += 1
            if token not in first_seen:
                first_seen[token] = para_idx
            if outside_heading:
                seen_outside_heading.add(token)
    items = [
        {"acronym": a, "count": c, "first_use_paragraph": first_seen[a], "used_once": c == 1}
        for a, c in counts.items()
        if a in seen_outside_heading
    ]
    items.sort(key=lambda x: (-x["count"], x["acronym"]))
    used_once = [i["acronym"] for i in items if i["used_once"]]
    return {
        "heuristic_note": "Regex heuristic on all-caps tokens; misses acronyms that double as common words and mixed-case abbreviations.",
        "low_confidence_note": "Low confidence: headings, Roman numerals, and code words also match; check each item.",
        "acronyms": items,
        "used_once_count": len(used_once),
        "used_once_list": used_once,
    }


def analyze_echoes(sentences: List[Sentence]) -> dict:
    repeated_word_hits = []
    for s in sentences:
        words = [t.lower() for t in s["tokens"] if len(t) > 3 and t.lower() not in STOPWORDS]
        counts = collections.Counter(words)
        repeats = {w: c for w, c in counts.items() if c >= 3}
        if repeats:
            repeated_word_hits.append({"text": s["text"], "para": s["para"], "words": repeats})
    adjacent_hits = []
    for i in range(1, len(sentences)):
        prev_tokens = sentences[i - 1]["tokens"]
        cur_tokens = sentences[i]["tokens"]
        if len(prev_tokens) >= 2 and len(cur_tokens) >= 2:
            if prev_tokens[0].lower() == cur_tokens[0].lower() and prev_tokens[1].lower() == cur_tokens[1].lower():
                adjacent_hits.append({
                    "first": {"text": sentences[i - 1]["text"], "para": sentences[i - 1]["para"]},
                    "second": {"text": sentences[i]["text"], "para": sentences[i]["para"]},
                })
    return {
        "heuristic_note": "Word-repetition and adjacent-opener heuristics; deliberate repetition for emphasis is flagged too.",
        "repeated_word_count": len(repeated_word_hits),
        "repeated_word_examples": repeated_word_hits,
        "adjacent_opener_count": len(adjacent_hits),
        "adjacent_opener_examples": adjacent_hits,
    }


def analyze_summary(sentences: List[Sentence], paragraphs: List[str], sections: dict) -> dict:
    words = [int(s["words"]) for s in sentences]
    n_sent = len(sentences)
    total_words = sum(words)
    mean_len = float(statistics.mean(words)) if words else 0.0
    median_len = float(statistics.median(words)) if words else 0.0
    longest = max(words) if words else 0
    over_30 = sum(1 for w in words if w > 30)
    over_40 = sum(1 for w in words if w > 40)
    share_30 = (over_30 / n_sent * 100) if n_sent else 0.0
    share_40 = (over_40 / n_sent * 100) if n_sent else 0.0
    passive_share_pct = sections["passive"]["share_of_sentences"] * 100
    return {
        "word_count": total_words,
        "sentence_count": n_sent,
        "paragraph_count": len(paragraphs),
        "mean_sentence_length": mean_len,
        "median_sentence_length": median_len,
        "longest_sentence_length": longest,
        "share_sentences_over_30_words": share_30,
        "share_sentences_over_40_words": share_40,
        "passive_candidate_share_pct": passive_share_pct,
        "clutter_phrase_count": sections["clutter"]["total_count"],
        "clutter_by_source": sections["clutter"]["by_source"],
        "hedge_count": sections["hedges"]["total_count"],
        "intensifier_count": sections["intensifiers"]["total_count"],
        "em_dash_count": sections["punctuation"]["em_dash_count"],
        "nominalization_density_per_100_words": sections["nominalizations"]["density_per_100_words"],
        "acronyms_used_once": sections["acronyms"]["used_once_count"],
    }


# ---------------------------------------------------------------------------
# Report assembly and formatting.
# ---------------------------------------------------------------------------

def build_report(text: str) -> dict:
    """Run every analyzer once and return one plain dict, keyed by section."""
    paragraphs = split_paragraphs(text)
    sentences = _build_sentences(paragraphs)
    all_words = [tok for s in sentences for tok in s["tokens"]]
    total_words = len(all_words)

    sections: dict = {}
    sections["long_sentences"] = analyze_long_sentences(sentences)
    sections["paragraphs"] = analyze_paragraphs(paragraphs, sentences)
    sections["passive"] = analyze_passive(sentences)
    sections["expletives"] = analyze_expletives(sentences)
    sections["nominalizations"] = analyze_nominalizations(all_words)
    sections["clutter"] = analyze_clutter(sentences)
    sections["hedges"] = analyze_hedges(sentences, total_words)
    sections["intensifiers"] = analyze_intensifiers(sentences)
    sections["vague_pronouns"] = analyze_vague_pronouns(sentences)
    sections["noun_strings"] = analyze_noun_strings(sentences)
    sections["punctuation"] = analyze_punctuation(sentences)
    sections["acronyms"] = analyze_acronyms(sentences, paragraphs)
    sections["echoes"] = analyze_echoes(sentences)
    sections["summary"] = analyze_summary(sentences, paragraphs, sections)
    return sections


# Which (section, key) list fields get trimmed to --top N at render time.
# build_report() itself stores full data; trimming happens only for display,
# identically for the text report and --json, so both show "the same content".
_TRIM_SPEC: List[Tuple[str, str]] = [
    ("long_sentences", "items"),
    ("passive", "examples"),
    ("expletives", "examples"),
    ("clutter", "phrases_found"),
    ("hedges", "stacked_examples"),
    ("intensifiers", "examples"),
    ("vague_pronouns", "examples"),
    ("noun_strings", "examples"),
    ("punctuation", "em_dash_examples"),
    ("acronyms", "acronyms"),
    ("echoes", "repeated_word_examples"),
    ("echoes", "adjacent_opener_examples"),
]


def _trimmed_copy(report: dict, top: int) -> dict:
    trimmed = copy.deepcopy(report)
    for section, key in _TRIM_SPEC:
        sec = trimmed.get(section)
        if sec and isinstance(sec.get(key), list):
            sec[key] = sec[key][:top]
    return trimmed


def _fmt(x: object) -> str:
    """One decimal place for floats, plain for everything else."""
    if isinstance(x, float):
        return f"{x:.1f}"
    return str(x)


def _format_summary_lines(s: dict) -> List[str]:
    return [
        "1. SUMMARY",
        f"  Words: {s['word_count']}  Sentences: {s['sentence_count']}  Paragraphs: {s['paragraph_count']}",
        f"  Mean sentence length: {_fmt(s['mean_sentence_length'])}  Median: {_fmt(s['median_sentence_length'])}  Longest: {s['longest_sentence_length']}",
        f"  Sentences over 30 words: {_fmt(s['share_sentences_over_30_words'])}%  Over 40 words: {_fmt(s['share_sentences_over_40_words'])}%",
        f"  Passive-candidate share of sentences: {_fmt(s['passive_candidate_share_pct'])}%",
        f"  Clutter phrases: {s['clutter_phrase_count']}  Hedges: {s['hedge_count']}  Intensifiers: {s['intensifier_count']}  Em dashes: {s['em_dash_count']}",
        "  Clutter by source: " + ", ".join(f"{label}: {count}" for label, count in s["clutter_by_source"].items()),
        f"  Nominalization density: {_fmt(s['nominalization_density_per_100_words'])} per 100 words",
        f"  Acronyms used exactly once: {s['acronyms_used_once']}",
    ]


def format_report(report: dict, top: int = 5) -> str:
    """Render the plain-text report. Applies --top trimming for display."""
    r = _trimmed_copy(report, top)
    lines: List[str] = ["Signals, not verdicts. A human decides.", ""]

    lines.extend(_format_summary_lines(r["summary"]))
    lines.append("")

    ls = r["long_sentences"]
    lines.append(f"2. LONG SENTENCES (top {top} of {len(report['long_sentences']['items'])})")
    lines.append(f"  {ls['note']}")
    for item in ls["items"]:
        lines.append(f"  [{item['words']}w, para {item['para']}] {item['text']}")
    lines.append("")

    pg = r["paragraphs"]
    lines.append("3. PARAGRAPHS")
    lines.append(f"  {pg['note']}")
    lines.append(f"  Word counts by paragraph: {pg['word_counts']}")
    lines.append(f"  Over 200 words: paragraphs {pg['over_200_words']}")
    lines.append(f"  Single-sentence paragraphs: {pg['single_sentence_paragraphs']}")
    lines.append("")

    pv = r["passive"]
    lines.append("4. PASSIVE-VOICE CANDIDATES")
    lines.append(f"  {pv['heuristic_note']}")
    lines.append(f"  Sentences flagged: {pv['sentence_count']}  Share of sentences: {_fmt(pv['share_of_sentences'] * 100)}%")
    for ex in pv["examples"]:
        lines.append(f"  [para {ex['para']}] {ex['text']}")
    lines.append("")

    ex_s = r["expletives"]
    lines.append("5. EXPLETIVE OPENERS")
    lines.append(f"  {ex_s['heuristic_note']}")
    lines.append(f"  Count: {ex_s['count']}")
    for ex in ex_s["examples"]:
        lines.append(f"  [para {ex['para']}] {ex['text']}")
    lines.append("")

    nm = r["nominalizations"]
    lines.append("6. NOMINALIZATIONS")
    lines.append(f"  {nm['note']}")
    lines.append(f"  Density: {_fmt(nm['density_per_100_words'])} per 100 words  Total: {nm['total_count']}")
    lines.append("  Ten most frequent:")
    for item in nm["top"]:
        lines.append(f"    {item['word']}: {item['count']}")
    lines.append("")

    cl = r["clutter"]
    lines.append(f"7. CLUTTER PHRASES (top {top} of {len(report['clutter']['phrases_found'])} phrases found)")
    lines.append(f"  {cl['heuristic_note']}")
    lines.append(f"  Total clutter-phrase count: {cl['total_count']}")
    for item in cl["phrases_found"]:
        flag = " [low-confidence]" if item["low_confidence"] else ""
        sources_str = ", ".join(item["sources"])
        instead = f" -- instead: {item['replacement']}" if item["replacement"] else ""
        lines.append(f"  \"{item['phrase']}\" ({sources_str}){flag}: {item['count']}x -- e.g. \"{item['example']}\"{instead}")
    lines.append("")

    hd = r["hedges"]
    lines.append("8. HEDGES")
    lines.append(f"  {hd['note']}")
    lines.append(f"  Total: {hd['total_count']}  Density: {_fmt(hd['density_per_100_words'])} per 100 words  Stacked sentences (2+): {hd['stacked_sentence_count']}")
    lines.append(f"  By word: {hd['by_word']}")
    for ex in hd["stacked_examples"]:
        lines.append(f"  [para {ex['para']}] {ex['text']}")
    lines.append("")

    it = r["intensifiers"]
    lines.append("9. INTENSIFIERS AND EMPTY MODIFIERS")
    lines.append(f"  {it['heuristic_note']}")
    lines.append(f"  Total: {it['total_count']}")
    lines.append(f"  By word: {it['by_word']}")
    for ex in it["examples"]:
        lines.append(f"  [para {ex['para']}] {ex['text']}")
    lines.append("")

    vp = r["vague_pronouns"]
    lines.append("10. SENTENCE-INITIAL VAGUE PRONOUNS")
    lines.append(f"  {vp['note']}")
    lines.append(f"  Count: {vp['count']}")
    for ex in vp["examples"]:
        lines.append(f"  [para {ex['para']}] {ex['text']}")
    lines.append("")

    ns = r["noun_strings"]
    lines.append("11. NOUN STRINGS (LOW CONFIDENCE)")
    lines.append(f"  {ns['heuristic_note']}")
    lines.append(f"  Count: {ns['count']}")
    for ex in ns["examples"]:
        lines.append(f"  [para {ex['para']}] \"{ex['run']}\" -- {ex['text']}")
    lines.append("")

    pu = r["punctuation"]
    lines.append("12. PUNCTUATION AND MECHANICS")
    lines.append(f"  {pu['heuristic_note']}")
    lines.append(f"  Em dashes: {pu['em_dash_count']}  Spaced en dashes: {pu['en_dash_spaced_count']}  Double hyphens: {pu['double_hyphen_count']}")
    lines.append(f"  Semicolons: {pu['semicolon_count']} ({_fmt(pu['semicolons_per_100_sentences'])} per 100 sentences)  Exclamation points: {pu['exclamation_count']}")
    lines.append(f"  Parentheses: {pu['parentheses_count']} ({_fmt(pu['parentheses_per_100_words'])} per 100 words)")
    lines.append(f"  Sentence-initial 'However': {pu['however_sentence_initial_count']}")
    lines.append(f"  'data is': {pu['data_is_count']}  'data are': {pu['data_are_count']}  'etc.': {pu['etc_count']}  'e.g.': {pu['eg_count']}  'i.e.': {pu['ie_count']}")
    for ex in pu["em_dash_examples"]:
        lines.append(f"  [para {ex['para']}] {ex['text']}")
    lines.append("")

    ac = r["acronyms"]
    lines.append("13. ACRONYMS")
    lines.append(f"  {ac['heuristic_note']}")
    lines.append(f"  {ac['low_confidence_note']}")
    lines.append(f"  Used exactly once: {ac['used_once_count']} {ac['used_once_list']}")
    for item in ac["acronyms"]:
        once = " (used once -- consider spelling out)" if item["used_once"] else ""
        lines.append(f"    {item['acronym']}: {item['count']}x, first used para {item['first_use_paragraph']}{once}")
    lines.append("")

    ec = r["echoes"]
    lines.append("14. ECHOES")
    lines.append(f"  {ec['heuristic_note']}")
    lines.append(f"  Repeated content word in one sentence (3+): {ec['repeated_word_count']}")
    for ex in ec["repeated_word_examples"]:
        lines.append(f"  [para {ex['para']}] {ex['words']} -- {ex['text']}")
    lines.append(f"  Adjacent sentences sharing their first two words: {ec['adjacent_opener_count']}")
    for pair in ec["adjacent_opener_examples"]:
        lines.append(f"  [para {pair['first']['para']}] {pair['first']['text']}")
        lines.append(f"  [para {pair['second']['para']}] {pair['second']['text']}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="prose_signals.py",
        description="Report mechanical prose signals in scientific writing. Signals, not verdicts; a human decides.",
    )
    parser.add_argument("paths", nargs="*", help="Input file(s): .txt, .md, or .docx. Reads stdin if omitted.")
    parser.add_argument("--json", action="store_true", help="Print a JSON object instead of the text report.")
    parser.add_argument("--top", type=int, default=5, help="Max examples shown per section (default 5).")
    parser.add_argument("--quiet", action="store_true", help="Print only the summary block.")
    args = parser.parse_args()

    text = load_text(args.paths)
    if not text or not text.strip():
        print("No text found in input.")
        return 0

    report = build_report(text)

    if args.json:
        trimmed = _trimmed_copy(report, args.top)
        print(json.dumps(trimmed, indent=2, ensure_ascii=False))
        return 0

    if args.quiet:
        lines = ["Signals, not verdicts. A human decides.", ""] + _format_summary_lines(report["summary"])
        print("\n".join(lines))
        return 0

    print(format_report(report, args.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
