#!/usr/bin/env python3
"""Self-tests for prose_signals.py. Plain asserts, no pytest.

Run: python3 scripts/test_prose_signals.py
"""
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prose_signals as ps  # noqa: E402

CLUTTERED = """
There is no doubt but that the data were collected in order to test the
hypothesis, and it was found that the results were affected by the fact
that temperature was not controlled during the trial. The effect might
perhaps somewhat likely be caused by drift, and it could also possibly be
related to humidity, pressure, or unmeasured confounds that were never
identified despite repeated attempts by the team to characterize them
fully across three separate facilities — a limitation the authors readily
acknowledge in the discussion section. This shows that the instrument was
not sufficiently stable for the full duration of the experiment. The
protocol was approved by the institutional review board (IRB) prior to
data collection. The measurements were taken every hour, and the values
were recorded by a technician who was not blinded to the treatment
condition, a design choice that was later identified as a serious flaw.
It is important to note that the sample size was small, and it should be
noted that replication is needed.
"""

CLEAN = """
We measured soil moisture at twelve sites every morning for six weeks.
Each sensor logged readings every ten minutes and stored them locally on
a memory card. We calibrated every sensor against a reference probe
before installation and checked calibration again after the study ended.
Rainfall explained most of the variation we observed across sites. Sites
near the river dried more slowly than sites on the ridge. We suspect
shallow groundwater buffers moisture near the river during dry spells,
and we plan to test that idea next season with additional wells. The
dataset includes over four hundred thousand readings, and we have posted
it publicly so other researchers can reuse it. Future work should add
temperature sensors at the same sites, since warmer soil speeds
evaporation.
"""

DOCX_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
<w:p><w:r><w:t>First paragraph text here.</w:t></w:r></w:p>
<w:p><w:r><w:t>Second paragraph text here.</w:t></w:r></w:p>
</w:body>
</w:document>"""


def test_cluttered_scores_higher_than_clean():
    r_c = ps.build_report(CLUTTERED)
    r_clean = ps.build_report(CLEAN)
    sc, sclean = r_c["summary"], r_clean["summary"]

    assert sc["clutter_phrase_count"] > sclean["clutter_phrase_count"], (
        sc["clutter_phrase_count"], sclean["clutter_phrase_count"])
    assert sclean["clutter_phrase_count"] == 0, sclean["clutter_phrase_count"]

    assert sc["passive_candidate_share_pct"] > sclean["passive_candidate_share_pct"], (
        sc["passive_candidate_share_pct"], sclean["passive_candidate_share_pct"])

    assert sc["hedge_count"] > sclean["hedge_count"], (sc["hedge_count"], sclean["hedge_count"])

    assert sc["em_dash_count"] > sclean["em_dash_count"], (
        sc["em_dash_count"], sclean["em_dash_count"])
    assert sclean["em_dash_count"] == 0, sclean["em_dash_count"]

    # Extra checks on features the CLUTTERED sample was built to contain.
    assert r_c["hedges"]["stacked_sentence_count"] >= 1
    assert r_c["expletives"]["count"] >= 1
    assert r_c["vague_pronouns"]["count"] >= 1
    assert r_c["acronyms"]["used_once_count"] >= 1
    assert r_c["summary"]["longest_sentence_length"] >= 40, r_c["summary"]["longest_sentence_length"]


def test_sentence_splitter_protects_abbreviations_and_decimals():
    para = (
        "As Smith et al. (2020) showed, the method works well. "
        "Fig. 2 shows the resulting trend. "
        "The increase was 3.5 percent over baseline."
    )
    sentences = ps.split_sentences(para)
    assert len(sentences) == 3, sentences
    assert any("et al. (2020) showed" in s for s in sentences), sentences
    assert any("Fig. 2 shows" in s for s in sentences), sentences
    assert any("3.5 percent" in s for s in sentences), sentences


def test_docx_loading_gives_two_paragraphs():
    fd, path = tempfile.mkstemp(suffix=".docx")
    os.close(fd)
    try:
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("word/document.xml", DOCX_XML)
        text = ps.load_text([path])
        paragraphs = ps.split_paragraphs(text)
        assert len(paragraphs) == 2, paragraphs
        assert "First paragraph" in paragraphs[0]
        assert "Second paragraph" in paragraphs[1]
    finally:
        os.remove(path)


def test_empty_input_handled():
    report = ps.build_report("")
    assert report["summary"]["word_count"] == 0
    assert report["summary"]["sentence_count"] == 0


def test_clutter_phrase_reports_all_sources():
    text = "The delay occurred due to the fact that the sensor failed."
    report = ps.build_report(text)
    hit = next(
        (p for p in report["clutter"]["phrases_found"] if p["phrase"] == "due to the fact that"),
        None,
    )
    assert hit is not None, report["clutter"]["phrases_found"]
    assert "general" in hit["sources"], hit["sources"]
    assert "Zinsser" in hit["sources"] or "Alley" in hit["sources"], hit["sources"]


def test_clutter_phrase_reports_heard_source():
    text = "The team conducted an analysis of the pooled samples."
    report = ps.build_report(text)
    hit = next(
        (p for p in report["clutter"]["phrases_found"] if p["phrase"] == "conducted an analysis"),
        None,
    )
    assert hit is not None, report["clutter"]["phrases_found"]
    assert "Heard" in hit["sources"], hit["sources"]


def test_roman_numeral_not_acronym():
    text = "This chapter covers background material. See Chapter II for the full derivation and worked examples."
    report = ps.build_report(text)
    names = [a["acronym"] for a in report["acronyms"]["acronyms"]]
    assert "II" not in names, names


def main():
    test_cluttered_scores_higher_than_clean()
    test_sentence_splitter_protects_abbreviations_and_decimals()
    test_docx_loading_gives_two_paragraphs()
    test_empty_input_handled()
    test_clutter_phrase_reports_all_sources()
    test_clutter_phrase_reports_heard_source()
    test_roman_numeral_not_acronym()
    print("all tests passed")


if __name__ == "__main__":
    main()
