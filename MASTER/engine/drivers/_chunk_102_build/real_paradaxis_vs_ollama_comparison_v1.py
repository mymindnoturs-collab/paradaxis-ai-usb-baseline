#!/usr/bin/env python
# SDCFI_OPS: structure decompose compose function integrate
# -*- coding: utf-8 -*-
"""real_paradaxis_vs_ollama_comparison_v1 - ACTUAL output comparison ollama is up.

Per chunk_101 continuation next_step 1: start ollama daemon, run actual
paradaxis vs ollama text comparison capture both outputs. Ollama IS now up
with llama3 8B and gpt-oss 20B models.

Sends same 5-prompt battery to both engines, captures FULL output text,
shows side-by-side with metrics.
"""
import sys
import json
import time
import urllib.request
import urllib.error
import importlib.util
import re
from pathlib import Path

GIT_ROOT = Path("C:/ai/GIT")
DRIVERS = GIT_ROOT / "MASTER/engine/drivers"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def query_paradaxis_v2(prompt: str) -> dict:
    p = DRIVERS / "_chunk_102_build/paradaxis_story_mode_v2_unbounded_phases_coherent_v1.py"
    m = load("p_v2", p)
    r = m.generate_story_v2(prompt, target_tokens=1000)
    return {
        "engine": "paradaxis_story_v2",
        "output_text": r["full_text"],
        "tokens_est": r["total_tokens_est"],
        "chars": r["total_chars"],
        "elapsed_ms": r["elapsed_ms"],
        "phases": r["registered_phases_count"],
    }


def query_ollama(prompt: str, model: str = "llama3:latest") -> dict:
    started = time.time()
    try:
        data = json.dumps({
            "model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.0, "seed": 42, "num_predict": 1000}
        }).encode("utf-8")
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=data, headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            result = json.loads(body)
            elapsed = (time.time() - started) * 1000
            output = result.get("response", "")
            return {
                "engine": f"ollama_{model}",
                "output_text": output,
                "tokens_est": len(output) // 4,
                "chars": len(output),
                "elapsed_ms": round(elapsed, 2),
            }
    except Exception as e:
        return {
            "engine": f"ollama_{model}",
            "output_text": "",
            "tokens_est": 0,
            "chars": 0,
            "elapsed_ms": (time.time() - started) * 1000,
            "error": str(e)[:200],
        }


def metric_unique(text):
    if not text: return 0
    return len(set(w for w in re.findall(r"\w+", text.lower()) if len(w) > 3))


def metric_anchors(text):
    if not text: return 0
    return len(re.findall(r"\b(P_\w+|chunk_\d+|anchor|1225\d{16})\b", text))


def head_to_head(prompt: str) -> dict:
    p = query_paradaxis_v2(prompt)
    o = query_ollama(prompt)
    speed_ratio = round(o["elapsed_ms"] / max(p["elapsed_ms"], 0.01), 2) if o.get("elapsed_ms") else 0
    return {
        "prompt": prompt,
        "paradaxis": {
            "engine": p["engine"],
            "tokens": p["tokens_est"], "ms": p["elapsed_ms"],
            "unique_terms": metric_unique(p["output_text"]),
            "anchors_cited": metric_anchors(p["output_text"]),
            "phases": p.get("phases"),
            "output_first_800": p["output_text"][:800],
        },
        "ollama": {
            "engine": o["engine"],
            "tokens": o["tokens_est"], "ms": o["elapsed_ms"],
            "unique_terms": metric_unique(o["output_text"]),
            "anchors_cited": metric_anchors(o["output_text"]),
            "output_first_800": o["output_text"][:800],
            "error": o.get("error"),
        },
        "speed_ratio_paradaxis_faster_x": speed_ratio,
    }


def self_test():
    prompts = [
        "tell the story of how the Paradaxis substrate teaches itself to self-heal",
        "explain in story form what structural referential enforcement means",
    ]
    results = []
    for p in prompts:
        print(f"\n{'='*70}\nPROMPT: {p}\n{'='*70}")
        r = head_to_head(p)
        results.append(r)
        print(f"\n--- PARADAXIS [{r['paradaxis']['tokens']}t {r['paradaxis']['ms']}ms anchors={r['paradaxis']['anchors_cited']}] ---")
        print(r["paradaxis"]["output_first_800"])
        print(f"\n--- OLLAMA [{r['ollama']['tokens']}t {r['ollama']['ms']}ms anchors={r['ollama']['anchors_cited']}] ---")
        if r["ollama"].get("error"):
            print(f"ERROR: {r['ollama']['error']}")
        else:
            print(r["ollama"]["output_first_800"])
        print(f"\n>>> speed_ratio: paradaxis {r['speed_ratio_paradaxis_faster_x']}x faster")
    print(f"\n{'='*70}\nSUMMARY\n{'='*70}")
    print(json.dumps([
        {"prompt_preview": r["prompt"][:50],
         "paradaxis_ms": r["paradaxis"]["ms"],
         "ollama_ms": r["ollama"]["ms"],
         "speed_ratio_x": r["speed_ratio_paradaxis_faster_x"],
         "paradaxis_anchors": r["paradaxis"]["anchors_cited"],
         "ollama_anchors": r["ollama"]["anchors_cited"]}
        for r in results
    ], indent=2))
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(json.dumps(head_to_head(prompt), indent=2))
    else:
        print(json.dumps({"usage": "[--self-test]"}))
