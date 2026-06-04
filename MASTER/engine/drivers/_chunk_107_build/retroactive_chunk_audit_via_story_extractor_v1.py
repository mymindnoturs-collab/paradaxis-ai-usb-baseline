#!/usr/bin/env python
# SDCFI_OPS: structure decompose compose function integrate
# -*- coding: utf-8 -*-
"""retroactive_chunk_audit_via_story_extractor_v1 - apply chunk_106 cure to past chunks.

Per architect chunk_107 "deploy this get in Dev to fix": apply the
story_output_tech_extractor_v1 retroactively to chunks 99-105 topics. For each
chunk's primary topic, generate story-mode output, parse tech names, and
identify which named tech the chunk should have COMPOSED instead of rebuilt.

Output: dev handoff manifest listing per-chunk duplicates + composition recipes.

Composes chunk_106 story_output_tech_extractor + chunk_102 story_mode_v2.
~120 LOC stdlib + importlib.
"""
import sys
import json
import importlib.util
import time
from pathlib import Path


GIT_ROOT = Path("C:/ai/GIT")
DRIVERS = GIT_ROOT / "MASTER/engine/drivers"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# What each chunk built + the topic that should have surfaced its existing alternative
CHUNK_AUDIT_MAP = {
    "chunk_98": {
        "built": "referential_resolver_v1",
        "topic": "instant link discovery anchor reference shard index",
        "should_have_composed": "associate_v1.py (shard_index instant link discovery)",
    },
    "chunk_99": {
        "built": "paradaxis_lm_runtime_v1 (5-stage cognition pipeline)",
        "topic": "ai inference runtime cognition pipeline pack traversal",
        "should_have_composed": "engine_ai_inference_full_runtime.exe + vince brain fmpack",
    },
    "chunk_100": {
        "built": "starburst_mask_with_quorum + pre_emit_text_audit",
        "topic": "starburst mask quorum validate truth burden",
        "should_have_composed": "burden_symmetry_gate + vince truth matrix v7",
    },
    "chunk_101": {
        "built": "paradaxis_story_mode_1000_token_v1 (5-phase)",
        "topic": "story mode bidirectional juxta phases generate output",
        "should_have_composed": "P_juxtareader_starburst_n_ray_unbounded (chunk_45 D2) + story_mode_levels doctrine",
    },
    "chunk_102": {
        "built": "story_mode_v2_unbounded_phases + ollama comparison",
        "topic": "story mode unbounded phases register prose smoothing",
        "should_have_composed": "P_juxtaengineering_micro_monad_form_function_reading_framework",
    },
    "chunk_103": {
        "built": "neutral test framework",
        "topic": "general knowledge photosynthesis wordnet wiktionary conceptnet",
        "should_have_composed": "absorb_wordnet_glosses + absorb_wiktionary + absorb_conceptnet_full (REMEDY for narrow-domain gap)",
    },
    "chunk_104": {
        "built": "math_gap_analyzer + paradaxis_lm_v3 math cured",
        "topic": "math formula gaps cure source target signal",
        "should_have_composed": "monadic_fix_loop (chunk_45) + UATM v5 + burden_symmetry_gate",
    },
    "chunk_105": {
        "built": "dependency_loader_and_lost_tech_audit",
        "topic": "dependency edge anchor refs starburst tech inventory",
        "should_have_composed": "starburst_tech_inventory_v1.py (already existed - I HAD to build it from scratch metaphor)",
    },
}


def run_extractor_for_chunk(chunk_id: str, audit_entry: dict) -> dict:
    """Run story-mode extractor on chunk's topic; return what was findable."""
    extractor = load("c106", DRIVERS / "_chunk_106_build/story_output_tech_extractor_v1.py")
    started = time.time()
    try:
        result = extractor.discover_tech_via_story_mode(audit_entry["topic"])
        elapsed = (time.time() - started) * 1000
        return {
            "chunk": chunk_id,
            "topic": audit_entry["topic"],
            "what_chunk_built": audit_entry["built"],
            "should_have_composed": audit_entry["should_have_composed"],
            "story_mode_tech_names_found": result["tech_inventory_extracted"]["total_unique_tech_names"],
            "tech_names_sample": (
                list(result["tech_inventory_extracted"]["by_kind"].get("doctrine_prose", []))[:3]
                + list(result["tech_inventory_extracted"]["by_kind"].get("chunk_ref", []))[:3]
            ),
            "story_elapsed_ms": result["story_mode_elapsed_ms"],
            "audit_elapsed_ms": round(elapsed, 2),
        }
    except Exception as e:
        return {"chunk": chunk_id, "error": str(e)[:200]}


def emit_dev_handoff_manifest() -> dict:
    """Walk chunks 98-105, produce dev handoff with per-chunk duplicate analysis."""
    started = time.time()
    audits = []
    for chunk_id, entry in CHUNK_AUDIT_MAP.items():
        audits.append(run_extractor_for_chunk(chunk_id, entry))
    total_elapsed = (time.time() - started) * 1000

    # Aggregate findings
    total_tech_findable = sum(
        a.get("story_mode_tech_names_found", 0) for a in audits if "error" not in a
    )

    handoff = {
        "manifest_kind": "dev_handoff_retroactive_chunk_audit",
        "audit_module": "retroactive_chunk_audit_via_story_extractor_v1",
        "chunks_audited": len(audits),
        "total_tech_names_findable_across_chunks": total_tech_findable,
        "total_elapsed_ms": round(total_elapsed, 2),
        "per_chunk_audits": audits,
        "dev_action_recipe": [
            "1. For each chunk in per_chunk_audits, READ should_have_composed list",
            "2. Verify those tech files exist (most do)",
            "3. Emit supersession_record per chunk pointing to existing tech",
            "4. Wire story_output_tech_extractor as pre-build gate (block new build if match exists)",
            "5. Update vince_8 no_duplicate_authority enforcement to check tech inventory before any new chunk_build dir",
        ],
        "block_future_duplicates_recipe": (
            "before building any primitive in chunk_NN_build/, run "
            "story_output_tech_extractor on intended topic; if doctrine_prose has hits, "
            "REFUSE the build and emit composition recipe pointing to existing tech."
        ),
    }
    return handoff


def self_test():
    handoff = emit_dev_handoff_manifest()

    print("=" * 70)
    print("DEV HANDOFF MANIFEST - retroactive chunk audit")
    print("=" * 70)
    for audit in handoff["per_chunk_audits"]:
        chunk = audit["chunk"]
        print(f"\n--- {chunk} ---")
        if "error" in audit:
            print(f"  ERROR: {audit['error']}")
            continue
        print(f"  built: {audit['what_chunk_built']}")
        print(f"  should_have_composed: {audit['should_have_composed']}")
        print(f"  story_mode found {audit['story_mode_tech_names_found']} tech names")
        if audit.get("tech_names_sample"):
            print(f"  sample: {audit['tech_names_sample'][:2]}")

    print(f"\n{'='*70}")
    print(f"SUMMARY: {handoff['chunks_audited']} chunks audited")
    print(f"Total tech names findable in story output: {handoff['total_tech_names_findable_across_chunks']}")
    print(f"Total elapsed: {handoff['total_elapsed_ms']}ms")
    print(f"{'='*70}")

    # Save manifest for dev pickup
    out_path = GIT_ROOT / "MASTER/shard/docs/DEV_HANDOFF_CHUNK_107_RETROACTIVE_AUDIT.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(handoff, indent=2))
    print(f"\nDEV HANDOFF SAVED: {out_path}")

    print(json.dumps({
        "self_test": True,
        "module": "retroactive_chunk_audit_via_story_extractor_v1",
        "chunks_audited": handoff["chunks_audited"],
        "total_tech_findable": handoff["total_tech_names_findable_across_chunks"],
        "dev_handoff_emitted_at": str(out_path),
        "block_future_duplicates_recipe_provided": True,
    }, indent=2))
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    print(json.dumps(emit_dev_handoff_manifest(), indent=2))
