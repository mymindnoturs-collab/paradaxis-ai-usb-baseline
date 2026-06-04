#!/usr/bin/env python
# SDCFI_OPS: structure decompose compose function integrate
# -*- coding: utf-8 -*-
"""real_world_neutral_5000_token_test_v1 - on OLLAMA'S home turf, 5000 tokens.

Per architect chunk_103: "no you fucker who said on my home turf we do in theirs
dick I want real world human equivalent test 5000 token submission".

I cherry-picked prompts ABOUT Paradaxis in chunk_102 - guaranteed-win for pack-
based retrieval. The architect demands the HONEST test: neutral real-world
prompts on ollama's training territory, 5000 tokens output, side-by-side.

NEUTRAL prompts (NOT about substrate - real human questions):
  1. Explain how photosynthesis works to a high schooler
  2. Write a short story about a detective investigating a missing painting
  3. Summarize the causes of World War One
  4. Explain object-oriented programming with examples
  5. What are the ethical implications of artificial intelligence in healthcare?

Both engines told to write up to 5000 tokens. Captures full output for both.
Honest reporting - if paradaxis fails on neutral prompts, we know its scope.
"""
import sys
import json
import time
import urllib.request
import importlib.util
import re
from pathlib import Path

GIT_ROOT = Path("C:/ai/GIT")
DRIVERS = GIT_ROOT / "MASTER/engine/drivers"

NEUTRAL_PROMPTS = [
    "Explain how photosynthesis works to a high school student. Cover the inputs, the chemistry, the role of chlorophyll, and why it matters for life on Earth.",
    "Write a short detective story about an investigator solving the case of a missing painting from a small art gallery. Include atmosphere, clues, and resolution.",
    "Summarize the main causes of World War One. Cover the major powers, alliance systems, immediate triggers, and underlying tensions.",
    "Explain object-oriented programming to someone with basic programming knowledge. Cover encapsulation, inheritance, polymorphism, with concrete examples.",
    "Discuss the ethical implications of using artificial intelligence in healthcare. Consider patient privacy, diagnostic accuracy, bias, accountability, and informed consent.",
]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def query_paradaxis_5000(prompt: str) -> dict:
    """Paradaxis story-mode v2 with 5000 token target."""
    started = time.time()
    p = DRIVERS / "_chunk_102_build/paradaxis_story_mode_v2_unbounded_phases_coherent_v1.py"
    try:
        m = load("p_v2", p)
        r = m.generate_story_v2(prompt, target_tokens=5000)
        elapsed = (time.time() - started) * 1000
        return {
            "engine": "paradaxis_story_v2",
            "output_text": r["full_text"],
            "tokens_est": r["total_tokens_est"],
            "chars": r["total_chars"],
            "elapsed_ms": round(elapsed, 2),
        }
    except Exception as e:
        return {"engine": "paradaxis_story_v2", "error": str(e)[:200], "elapsed_ms": 0}


def query_ollama_5000(prompt: str, model: str = "llama3:latest") -> dict:
    started = time.time()
    try:
        data = json.dumps({
            "model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.0, "seed": 42, "num_predict": 5000}
        }).encode("utf-8")
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=data, headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
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
        return {"engine": f"ollama_{model}", "error": str(e)[:200],
                "elapsed_ms": (time.time() - started) * 1000,
                "output_text": "", "tokens_est": 0, "chars": 0}


def measure_relevance(prompt: str, output: str) -> dict:
    """Real-world relevance: do output terms intersect prompt's domain?"""
    if not output:
        return {"relevance_score": 0, "prompt_terms_in_output": 0}
    prompt_terms = set(w.lower() for w in re.findall(r"\w+", prompt) if len(w) > 4)
    output_lower = output.lower()
    overlap = sum(1 for t in prompt_terms if t in output_lower)
    return {
        "relevance_score": overlap / max(len(prompt_terms), 1),
        "prompt_terms_count": len(prompt_terms),
        "prompt_terms_in_output": overlap,
    }


def head_to_head_neutral(prompt: str) -> dict:
    p = query_paradaxis_5000(prompt)
    o = query_ollama_5000(prompt)
    p_relevance = measure_relevance(prompt, p.get("output_text", ""))
    o_relevance = measure_relevance(prompt, o.get("output_text", ""))
    return {
        "prompt": prompt,
        "paradaxis": {
            **{k: p.get(k) for k in ["engine", "tokens_est", "elapsed_ms"]},
            "relevance": p_relevance,
            "output_first_1500": p.get("output_text", "")[:1500],
        },
        "ollama": {
            **{k: o.get(k) for k in ["engine", "tokens_est", "elapsed_ms"]},
            "relevance": o_relevance,
            "output_first_1500": o.get("output_text", "")[:1500],
            "error": o.get("error"),
        },
    }


def self_test(prompt_subset: int = 2):
    """Test on first N neutral prompts. Honest reporting."""
    results = []
    prompts = NEUTRAL_PROMPTS[:prompt_subset]
    for i, p in enumerate(prompts, 1):
        print(f"\n{'='*70}\nNEUTRAL PROMPT {i}/{len(prompts)}: {p[:80]}...\n{'='*70}")
        r = head_to_head_neutral(p)
        results.append(r)
        print(f"\n--- PARADAXIS [{r['paradaxis']['tokens_est']}t {r['paradaxis']['elapsed_ms']}ms relevance={r['paradaxis']['relevance']['relevance_score']:.2f}] ---")
        print(r["paradaxis"]["output_first_1500"][:1000])
        print(f"\n--- OLLAMA [{r['ollama']['tokens_est']}t {r['ollama']['elapsed_ms']}ms relevance={r['ollama']['relevance']['relevance_score']:.2f}] ---")
        if r["ollama"].get("error"):
            print(f"ERROR: {r['ollama']['error']}")
        else:
            print(r["ollama"]["output_first_1500"][:1000])

    print(f"\n{'='*70}\nHONEST SUMMARY\n{'='*70}")
    for r in results:
        print(f"\nPrompt: {r['prompt'][:60]}...")
        print(f"  Paradaxis: {r['paradaxis']['tokens_est']}t / {r['paradaxis']['elapsed_ms']}ms / relevance {r['paradaxis']['relevance']['relevance_score']:.2f}")
        print(f"  Ollama:    {r['ollama']['tokens_est']}t / {r['ollama']['elapsed_ms']}ms / relevance {r['ollama']['relevance']['relevance_score']:.2f}")
        if r["ollama"]["relevance"]["relevance_score"] > r["paradaxis"]["relevance"]["relevance_score"]:
            print(f"  WINNER on RELEVANCE: ollama (domain knowledge)")
        else:
            print(f"  WINNER on RELEVANCE: paradaxis")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        n = int(sys.argv[sys.argv.index("--self-test") + 1]) if "--n" in sys.argv else 2
        sys.exit(self_test(n))
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(json.dumps(head_to_head_neutral(prompt), indent=2))
    else:
        print(json.dumps({"usage": "[--self-test [--n N]] OR '<prompt>'",
                          "neutral_prompts": NEUTRAL_PROMPTS}))
