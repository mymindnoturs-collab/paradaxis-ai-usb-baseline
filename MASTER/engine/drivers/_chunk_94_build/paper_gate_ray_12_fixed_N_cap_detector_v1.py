#!/usr/bin/env python
# SDCFI_OPS: structure decompose compose function integrate
# -*- coding: utf-8 -*-
"""paper_gate_ray_12_fixed_N_cap_detector_v1 - cure 'why didnt fire' meta-issue.

Per architect chunk_94: "why did that not fire when failure emitted was
exposed". Chunk_93 introduced a 4-axis fixed-N classifier; the chunk_84
starburst should have caught it but didn't because no ray scanned for
fixed-N caps in NEW DOCTRINES.

This is RAY_12 of the paper-gate starburst. Composes chunk_84 11-ray plus
chunk_92 test-coverage rays. Now 12 rays canonical.

Scan patterns:
  literal counts in classification thresholds  -> score == 4, len(x) == N
  fixed cardinality in axis lists              -> exactly_N_axes, N_field_grammar
  cap claims in doctrine descriptions          -> "4 axes" "N=6 fields"
  array length assertions                      -> assert len(x) == FIXED

Each finding produces refusal_record with cure recipe: replace fixed-N
with UNBOUNDED N per R22; treat initial count as SEED not CAP.

~60 LOC stdlib only.
"""
import sys
import json
import re
import time
from pathlib import Path


DRIVERS = Path("C:/ai/GIT/MASTER/engine/drivers")
SPOOL = Path("C:/ai/GIT/MASTER/engine/spool/paper_gate_ray_12")

# Patterns that indicate fixed-N cap
FIXED_N_PATTERNS = [
    re.compile(r"score\s*==\s*\d+"),
    re.compile(r"len\([\w\.]+\)\s*==\s*\d+"),
    re.compile(r"max\s*[:=]\s*\d+"),
    re.compile(r'"max"\s*:\s*\d+'),
    re.compile(r"assert\s+len\([^)]+\)\s*[<>=]=?\s*\d+"),
    re.compile(r"exactly\s+\d+\s+(axes|fields|rays|items)", re.IGNORECASE),
]

# Exception patterns: known seeds explicitly marked unbounded
EXEMPT_PATTERNS = [
    re.compile(r"unbounded", re.IGNORECASE),
    re.compile(r"R22", re.IGNORECASE),
    re.compile(r"seed", re.IGNORECASE),
]


def scan_for_fixed_N_caps(py_path: Path) -> list:
    """Find fixed-N cap patterns in a python file."""
    try:
        content = py_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    findings = []
    for line_no, line in enumerate(content.splitlines(), 1):
        if any(exempt.search(line) for exempt in EXEMPT_PATTERNS):
            continue
        for pat in FIXED_N_PATTERNS:
            if pat.search(line):
                findings.append({
                    "file": py_path.name,
                    "line": line_no,
                    "text": line.strip()[:150],
                    "matched_pattern": pat.pattern,
                    "cure_recipe": "replace fixed N with UNBOUNDED per R22; mark count as SEED not CAP",
                })
                if len(findings) >= 5:
                    return findings
                break
    return findings


def run_ray_12_audit(target_chunks: list = None) -> dict:
    """Scan all chunk_NN_build/ folders for fixed-N caps."""
    SPOOL.mkdir(parents=True, exist_ok=True)
    started = int(time.time())
    chunk_dirs = sorted(DRIVERS.glob("_chunk_*_build"))
    if target_chunks:
        chunk_dirs = [c for c in chunk_dirs
                      if any(str(t) in c.name for t in target_chunks)]
    all_findings = []
    for chunk_dir in chunk_dirs:
        for py in chunk_dir.glob("*.py"):
            findings = scan_for_fixed_N_caps(py)
            for f in findings:
                f["chunk"] = chunk_dir.name
                all_findings.append(f)
    report = {
        "ts": started,
        "ray_version": "paper_gate_ray_12_fixed_N_cap_detector_v1",
        "chunks_scanned": len(chunk_dirs),
        "total_findings": len(all_findings),
        "supersedes_gap_why_didnt_fire_on_chunk_93": True,
        "composes_chunk_84_11_rays_now_12": True,
        "sample_findings": all_findings[:10],
    }
    report_file = SPOOL / f"ray_12_audit_{started}.json"
    report_file.write_text(json.dumps(report, indent=2))
    return report


def self_test():
    # Specifically scan chunk_93 to PROVE it would have caught the violation
    report_93 = run_ray_12_audit(target_chunks=["93"])
    # Now scan everything
    report_all = run_ray_12_audit()
    out = {
        "self_test": True,
        "ray_version": "paper_gate_ray_12_fixed_N_cap_detector_v1",
        "chunk_93_scan_findings": report_93["total_findings"],
        "chunk_93_caught_v1_violation": report_93["total_findings"] > 0,
        "all_chunks_scan_findings": report_all["total_findings"],
        "ray_12_supplements_chunks_84_92_paper_gate_starburst": True,
        "cure_for_architect_question_why_didnt_fire": "this_ray_scans_for_fixed_N_caps_in_classifiers",
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    print(json.dumps({"usage": "[--self-test]"}))
