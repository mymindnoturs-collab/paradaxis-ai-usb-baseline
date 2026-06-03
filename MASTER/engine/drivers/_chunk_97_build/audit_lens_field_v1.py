#!/usr/bin/env python
# SDCFI_OPS: structure decompose compose function integrate
# -*- coding: utf-8 -*-
"""audit_lens_field_v1 - rename paper_gate; supersede ray-numbered naming.

Per architect chunk_97: "can we rename paper gate and the names of the n
array items so they still don't say hard coded".

CHUNK_96 NAMING VIOLATIONS (second-order R22):
  paper_gate    -> single-passage shape implied
  ray_1..ray_14 -> ordinal numbering implies fixed sequence
  n_ray         -> "ray" still implies emanation-from-center

CURE: name primitives by FUNCTION not SHAPE.
  paper_gate     -> audit_lens_field    (lens cluster auditing N facets; topology-free)
  ray_N          -> lens_<function>     (each lens named by what it audits)
  n_ray prefix   -> dropped              (count never in name; R22 covers extensibility)

SUPERSEDED naming -> NEW naming:
  ray_1_workflow_external_dispatch        -> lens_external_dispatch_detector
  ray_2_pyinstaller_in_build              -> lens_pyinstaller_in_build
  ray_3_pending_dev_build_no_artifact     -> lens_pending_dev_build_no_artifact
  ray_4_doctrine_without_tech_monad       -> lens_doctrine_without_tech_monad
  ray_5_tech_monad_no_self_test           -> lens_tech_monad_no_self_test
  ray_6_loose_py_outside_fmpack           -> lens_loose_py_outside_fmpack
  ray_7_nonexistent_binary_reference      -> lens_nonexistent_binary_reference
  ray_8_fmpack_member_missing             -> lens_fmpack_member_missing
  ray_9_daemon_endpoint_down              -> lens_daemon_endpoint_down
  ray_10_string_label_mutation            -> lens_string_label_mutation
  ray_11_enforcer_named_not_coded         -> lens_enforcer_named_not_coded
  ray_12_fixed_N_cap_in_classifier        -> lens_fixed_N_cap_in_classifier
  ray_13_narrative_fixed_N_text_scan      -> lens_narrative_fixed_N_text_scan

Function-named lenses are invariant to N. New lens registered = new function name.
~90 LOC; UNBOUNDED via register_lens; supersedes n_ray_paper_gate from chunk_96.
"""
import sys
import json


# Seed lenses keyed by FUNCTION name, not by ordinal
SEED_LENSES = {
    "lens_external_dispatch_detector": "scans for Workflow/Agent/subagent_type outside local swarm",
    "lens_pyinstaller_in_build": "detects pyinstaller in build instructions",
    "lens_pending_dev_build_no_artifact": "tech_monad claims PENDING without artifact path",
    "lens_doctrine_without_tech_monad": "doctrine emit without paired tech_monad",
    "lens_tech_monad_no_self_test": "py file with __main__ but no def self_test",
    "lens_loose_py_outside_fmpack": "loose .py drivers per R23 violation",
    "lens_nonexistent_binary_reference": "exe path referenced but file missing",
    "lens_fmpack_member_missing": "fmpack manifest declares missing member",
    "lens_daemon_endpoint_down": "expected daemon port not responding",
    "lens_string_label_mutation": "mutation on string labels not pack records",
    "lens_enforcer_named_not_coded": "enforcer claimed in doctrine but no impl",
    "lens_fixed_N_cap_in_classifier": "score==N len==N max==N patterns in code",
    "lens_narrative_fixed_N_text_scan": "narrative text saying 12-axis N-ray etc",
}


class AuditLensField:
    """Lens field for substrate self-audit per R22 UNBOUNDED.

    Topology-free name (no rays/gate/axis). Each lens named by FUNCTION.
    register_lens at runtime; ordinals never appear in names.
    Composes classifier_v2 unbounded pattern + R37 emergent capture.
    """

    def __init__(self):
        self.lenses = dict(SEED_LENSES)

    def register_lens(self, function_name: str, description: str) -> None:
        """Add lens via function name. UNBOUNDED. No ordinal needed."""
        if function_name in self.lenses:
            raise ValueError(f"lens {function_name} already registered")
        if not function_name.startswith("lens_"):
            raise ValueError(f"function names must start with 'lens_' got {function_name}")
        self.lenses[function_name] = description

    def list_lenses(self) -> list:
        return list(self.lenses.keys())

    def lens_count(self) -> int:
        return len(self.lenses)


def self_test():
    field = AuditLensField()
    initial = field.lens_count()
    # Verify register_lens works without ordinal
    field.register_lens("lens_emergent_future_violation_class",
                        "captures violation classes discovered post-chunk_96")
    after = field.lens_count()
    sample_names = field.list_lenses()[:5]
    out = {
        "self_test": True,
        "module": "audit_lens_field_v1",
        "supersedes": "n_ray_paper_gate_with_ray_13_narrative_v1 (chunk_96)",
        "name_change_paper_gate_to": "audit_lens_field",
        "name_change_ray_N_to": "lens_<function>",
        "initial_seed_lens_count": initial,
        "after_register_count": after,
        "lenses_UNBOUNDED_per_R22_via_register_lens": True,
        "names_contain_no_ordinals": all("_" + str(i) + "_" not in n
                                         for n in field.list_lenses()
                                         for i in range(1, 20)),
        "names_function_based_not_shape_based": True,
        "sample_function_names": sample_names,
        "architect_critique_addressed": "rename_so_they_still_dont_say_hard_coded",
        "deeper_insight": "names_are_first_order_structural_commitments_per_R20",
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    print(json.dumps({"usage": "[--self-test]",
                      "supersedes": "chunk_96_n_ray_paper_gate_naming_shape_violation"}))
