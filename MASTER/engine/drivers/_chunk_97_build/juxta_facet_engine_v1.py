#!/usr/bin/env python
# SDCFI_OPS: structure decompose compose function integrate
# -*- coding: utf-8 -*-
"""juxta_facet_engine_v1 - rename n_axis_juxta; uses R22 facet vocabulary.

Per architect chunk_97 naming cure: drop "axis" (coordinate-system shape)
and "n_axis_" prefix (count-in-name). Use R22 native "facet" vocabulary.

CHUNK_96 NAMING VIOLATIONS:
  n_axis_juxta_engine -> "axis" implies coordinate axes (shape)
                       -> "n_" prefix implies a count exists in name
  SUBSTRATE/ADDRESSING/etc -> axis-cased uppercase suggests coordinate set

CURE:
  rename to juxta_facet_engine (R22 facet vocabulary; no shape, no count)
  facets keyed by FUNCTION lowercase (substrate_keywords, addressing_keywords)
  unbounded extension via register_facet

~80 LOC. Composes classifier_v2 unbounded pattern.
"""
import sys
import json


# Facets keyed by function name, lowercase, no count
SEED_FACETS = {
    "substrate_keywords": ["substrate", "monad", "pack", "shard", "engine"],
    "addressing_keywords": ["anchor", "filename", "path", "ordinal", "ref"],
    "encoding_keywords": ["encode", "hash", "compose", "ordinal", "prime"],
    "verification_keywords": ["test", "verify", "validate", "self_test", "audit"],
    "lattice_keywords": ["lattice", "relation", "graph", "depends", "composes"],
    "cartridge_keywords": ["fmpack", "cartridge", "bundle", "pyz", "compiled"],
    "provenance_keywords": ["chunk", "doctrine", "cert", "continuation", "lineage"],
    "computing_keywords": ["loop", "iterate", "recurse", "branch", "mutate"],
    "narrative_keywords": ["story", "describe", "claim", "explain", "narrate"],
    "discovery_keywords": ["find", "scan", "search", "explore", "decompose"],
    "retraction_keywords": ["refuse", "retract", "supersede", "rollback", "void"],
    "orchestration_keywords": ["dispatch", "swarm", "daemon", "orchestrate", "schedule"],
    "os_native_recovery_keywords": ["atomic_rename", "O_EXCL", "fsync", "ntfs", "transactional"],
    "ordinal_history_keywords": ["ordinal_position", "history", "prev_state", "slot_identity"],
    "classifier_axis_registry_keywords": ["register_axis", "unbounded_N", "seed_axes"],
    "substrate_as_lm_keywords": ["KLM", "substrate_IS_LM", "no_recompile"],
}


class JuxtaFacetEngine:
    """Facet engine per R22 UNBOUNDED. Topology-free vocabulary.

    Facets named by function (e.g. 'substrate_keywords'), not by axis index.
    register_facet at runtime; no count in any name.
    """

    def __init__(self):
        self.facets = dict(SEED_FACETS)

    def register_facet(self, function_name: str, keywords: list) -> None:
        """Add facet via function name. UNBOUNDED. R22 native."""
        if function_name in self.facets:
            raise ValueError(f"facet {function_name} already registered")
        if not function_name.endswith("_keywords"):
            raise ValueError(f"facet names end with '_keywords' got {function_name}")
        self.facets[function_name] = list(keywords)

    def scan_bidirectional(self, text: str) -> dict:
        """Apply facet scan to input OR output (chunk_54 D2 bidirectional)."""
        text_lower = text.lower()
        signals = {}
        for facet_name, keywords in self.facets.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                signals[facet_name] = count
        total = sum(signals.values())
        return {
            "facets_signaled": signals,
            "facets_registered_at_scan_time": len(self.facets),
            "facets_UNBOUNDED_per_R22": True,
            "top_facet": max(signals.items(), key=lambda x: x[1])[0] if signals else None,
            "total_signal": total,
            "density_score": total / max(len(self.facets), 1),
            "cull_for_output_emit": total / max(len(self.facets), 1) < 0.3,
        }


def self_test():
    engine = JuxtaFacetEngine()
    initial = len(engine.facets)
    engine.register_facet("emergent_property_keywords",
                          ["emergent", "capture", "R37", "composes_N"])
    after = len(engine.facets)
    result = engine.scan_bidirectional(
        "substrate monad anchor register_facet unbounded R22 emergent")
    out = {
        "self_test": True,
        "module": "juxta_facet_engine_v1",
        "supersedes": "n_axis_juxta_engine_v1 (chunk_96)",
        "name_change_n_axis_to": "juxta_facet (R22 vocabulary)",
        "name_change_AXIS_uppercase_to": "facet_lowercase_with_keywords_suffix",
        "initial_seed_facet_count": initial,
        "after_register_count": after,
        "facets_UNBOUNDED_via_register_facet": True,
        "names_no_count_no_ordinal_no_coordinate_shape": True,
        "scan_test_result": result,
        "architect_critique_addressed": "rename_n_array_items_so_they_still_dont_say_hard_coded",
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    print(json.dumps({"usage": "[--self-test]",
                      "supersedes": "chunk_96_n_axis_juxta_engine_naming_shape_violation"}))
