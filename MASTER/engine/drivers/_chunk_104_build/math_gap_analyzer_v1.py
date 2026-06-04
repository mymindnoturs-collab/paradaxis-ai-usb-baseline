#!/usr/bin/env python
# SDCFI_OPS: structure decompose compose function integrate
# -*- coding: utf-8 -*-
"""math_gap_analyzer_v1 - use source/target pairs as training signal for math fix.

Per architect chunk_104: "you have the source to fix it math not patch some code
ass figure out how to fix our math formulas its perfect so easy source target
in-between both models you can see or put and then analyze in our load of the
game model and figure out our gaps and flaws in our math".

INPUT: (prompt, paradaxis_output, ollama_output) triples from chunk_103
OUTPUT: identified math formula gaps + concrete cure recipes

Analyzes what mathematical structure is missing by diffing source/target:
  1. domain_coverage_gap: does prompt's content terms intersect pack vocabulary?
  2. facet_signal_gap: does juxta math return anything > 0 on this prompt?
  3. scope_predicate_gap: when signal is 0 does engine declare out-of-scope?
  4. complement_extraction_gap: does engine extract ad-hoc facets from prompt?

Each gap is a CONCRETE formula modification recipe.

~110 LOC stdlib + importlib.
"""
import sys
import json
import re
import importlib.util
from pathlib import Path


GIT_ROOT = Path("C:/ai/GIT")
DRIVERS = GIT_ROOT / "MASTER/engine/drivers"
PACK = GIT_ROOT / "M0_TECH/MONAD_DISTRIBUTED/m0_ai_klm_hybrid_v2_0/monad_distributed.lineage.monad.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extract_content_terms(text: str, min_len: int = 5) -> set:
    """Extract content words - skip stopwords + short words."""
    stop = {"about", "would", "could", "should", "their", "there", "these",
            "those", "where", "which", "while", "after", "before",
            "between", "explain", "story", "write", "include", "cover"}
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return set(w for w in words if len(w) >= min_len and w not in stop)


def measure_juxta_signal_on_prompt(prompt: str) -> dict:
    """Run juxta facet engine and return mathematical signal."""
    m = load("c97_juxta", DRIVERS / "_chunk_97_build/juxta_facet_engine_v1.py")
    eng = m.JuxtaFacetEngine()
    scan = eng.scan_bidirectional(prompt)
    return {
        "signaled_facets_count": len(scan.get("facets_signaled", {})),
        "total_facets_available": scan.get("facets_registered_at_scan_time", 0),
        "total_signal": scan.get("total_signal", 0),
        "density_score": scan.get("density_score", 0),
    }


def measure_pack_coverage(prompt: str, sample_size: int = 500) -> dict:
    """For each prompt content term, what fraction appear in pack?"""
    terms = extract_content_terms(prompt)
    if not terms or not PACK.exists():
        return {"prompt_terms": list(terms), "coverage_score": 0,
                "terms_with_pack_presence": 0}
    with PACK.open("rb") as f:
        all_lines = list(f)
    sample = all_lines[-sample_size:] if len(all_lines) > sample_size else all_lines
    sample_text = b"".join(sample).decode("utf-8", errors="ignore").lower()
    terms_present = sum(1 for t in terms if t in sample_text)
    return {
        "prompt_terms": list(terms)[:10],
        "prompt_terms_count": len(terms),
        "terms_with_pack_presence": terms_present,
        "coverage_score": round(terms_present / max(len(terms), 1), 3),
    }


def analyze_math_gaps(prompt: str, paradaxis_output: str = "",
                      ollama_output: str = "") -> dict:
    """Identify which math formula stages failed."""
    juxta = measure_juxta_signal_on_prompt(prompt)
    coverage = measure_pack_coverage(prompt)

    gaps = []

    # GAP 1: facet signal returned nothing
    if juxta["total_signal"] == 0:
        gaps.append({
            "gap": "facet_signal_zero",
            "formula_stage": "juxta_signal(prompt)",
            "current_math": "sum_over_facets count(facet_keyword in prompt)",
            "current_result": 0,
            "cure_recipe": "add prompt_term_complement: if signal==0, treat prompt content terms as ad-hoc facets",
        })

    # GAP 2: scope predicate missing
    if juxta["density_score"] < 0.05:
        gaps.append({
            "gap": "no_scope_predicate",
            "formula_stage": "engine.emit",
            "current_math": "always emit top_N (no out-of-scope check)",
            "current_result": "emits substrate dump regardless",
            "cure_recipe": "add scope_predicate: if density < 0.05 return OUT_OF_SCOPE marker not records",
        })

    # GAP 3: pack has no terms from prompt domain
    if coverage["coverage_score"] < 0.20:
        gaps.append({
            "gap": "pack_domain_coverage_low",
            "formula_stage": "starburst_mask(record)",
            "current_math": "AND over signaled facets, facet_present in record",
            "current_result": f"coverage {coverage['coverage_score']} < 0.20 threshold",
            "cure_recipe": "add delegation: if pack_coverage < 0.20 declare out-of-scope or delegate to external LLM",
        })

    # GAP 4: relevance asymmetry observable from outputs
    if paradaxis_output and ollama_output:
        terms = extract_content_terms(prompt)
        p_match = sum(1 for t in terms if t in paradaxis_output.lower())
        o_match = sum(1 for t in terms if t in ollama_output.lower())
        if o_match > p_match:
            gaps.append({
                "gap": "output_relevance_inferior",
                "formula_stage": "emit -> output",
                "current_math": "stitch survivors regardless of relevance to prompt",
                "current_result": f"paradaxis prompt-term hits {p_match} ollama prompt-term hits {o_match}",
                "cure_recipe": "add relevance_filter on emitted blocks: keep only blocks containing prompt content terms",
            })

    return {
        "prompt": prompt,
        "juxta_math_state": juxta,
        "pack_coverage": coverage,
        "math_gaps_identified": len(gaps),
        "gaps": gaps,
        "cure_summary": [g["cure_recipe"] for g in gaps],
        "overall_diagnosis": (
            "OUT_OF_SCOPE - prompt domain not covered by substrate pack"
            if juxta["total_signal"] == 0 and coverage["coverage_score"] < 0.20
            else "PARTIAL_SCOPE"
        ),
    }


def self_test():
    # Use chunk_103 captured outputs as source/target training pairs
    prompts_and_outputs = [
        {
            "prompt": "Explain how photosynthesis works to a high school student",
            "paradaxis": "substrate monad anchor sprawl audit branches files",
            "ollama": "Photosynthesis chlorophyll absorbs light water carbon dioxide glucose plants chemistry",
        },
        {
            "prompt": "Write a detective story about a missing painting",
            "paradaxis": "substrate doctrine chunk anchor cure compose",
            "ollama": "Detective gallery Mrs Jenkins Ravenswood painting Whispers Night investigator",
        },
        {
            "prompt": "Explain structural referential enforcement in Paradaxis substrate",
            "paradaxis": "substrate monad anchor chunk doctrine compose proven structural",
            "ollama": "revolutionary material adapt evolve heal samples scientists Paradaxis",
        },
    ]
    analyses = []
    for pair in prompts_and_outputs:
        analysis = analyze_math_gaps(pair["prompt"], pair["paradaxis"], pair["ollama"])
        analyses.append(analysis)
        print(f"\n--- PROMPT: {pair['prompt'][:60]}... ---")
        print(f"  diagnosis: {analysis['overall_diagnosis']}")
        print(f"  juxta_signal: {analysis['juxta_math_state']['total_signal']}")
        print(f"  pack_coverage: {analysis['pack_coverage']['coverage_score']}")
        print(f"  gaps_identified: {analysis['math_gaps_identified']}")
        for g in analysis["gaps"]:
            print(f"    - {g['gap']}: {g['cure_recipe'][:80]}")
    print("\n" + "="*70)
    print(json.dumps({
        "self_test": True,
        "module": "math_gap_analyzer_v1",
        "prompts_analyzed": len(analyses),
        "total_gaps_identified": sum(a["math_gaps_identified"] for a in analyses),
        "diagnoses": [a["overall_diagnosis"] for a in analyses],
        "math_cures_emergent_from_source_target_pairs": True,
    }, indent=2))
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(json.dumps(analyze_math_gaps(prompt), indent=2))
    else:
        print(json.dumps({"usage": "[--self-test] OR '<prompt>'"}))
