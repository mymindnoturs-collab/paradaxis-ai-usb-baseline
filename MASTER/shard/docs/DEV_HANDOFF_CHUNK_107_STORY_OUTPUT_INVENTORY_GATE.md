# Dev Handoff — chunk_107 — Story-Output-Inventory Pre-Build Gate

## Source

- chunk_106 doctrine: `1225330018947694695` (story output IS inventory signal)
- chunk_107 objective: pending emit this turn
- audit manifest JSON: `DEV_HANDOFF_CHUNK_107_RETROACTIVE_AUDIT.json` (same folder)

## What you're being handed

A working extractor + retroactive audit + a request to wire the extractor into the pre-build pipeline so duplicate-building becomes structurally impossible.

## The problem in one sentence

Across chunks 98-105 the designer built **8 primitives that duplicate existing substrate tech**. Story-mode v2 was emitting the canonical tech names in its own output the whole time. The designer treated them as content instead of as a discovery signal.

## What to build

A pre-build gate that fires before any `chunk_NN_build/<new_primitive>.py` is written:

```
1. Parse intended primitive's docstring/topic from filename grammar (R20).
2. Run paradaxis_story_mode_v2.generate_story_v2(topic, target_tokens=1000).
3. Run story_output_tech_extractor_v1.extract_tech_inventory_from_text(story_output).
4. If extractor returns N>=3 doctrine_prose matches:
     - Emit refusal_record with reason="story-output reveals existing tech"
     - Print composition recipe pointing to those P_* names
     - REFUSE the build (R47 fix-or-refuse)
5. Else: allow build.
```

Per `vince_8 no_duplicate_authority` this becomes structural.

## Retroactive findings — what each chunk should have composed

| Chunk | Built | Should have composed |
|---|---|---|
| chunk_98 | referential_resolver_v1 | `associate_v1.py` (shard_index instant link discovery) |
| chunk_99 | paradaxis_lm_runtime_v1 (5-stage cognition) | `engine_ai_inference_full_runtime.exe` + vince brain fmpack |
| chunk_100 | starburst_mask_with_quorum + pre_emit_text_audit | `burden_symmetry_gate` + vince truth matrix v7 |
| chunk_101 | story_mode_1000_token_v1 (fixed 5-phase) | `P_juxtareader_starburst_n_ray_unbounded` (chunk_45 D2) + story_mode_levels doctrine |
| chunk_102 | story_mode_v2 + ollama comparison | `P_juxtaengineering_micro_monad_form_function_reading_framework` |
| chunk_103 | neutral test framework | `absorb_wordnet_glosses` + `absorb_wiktionary` + `absorb_conceptnet_full` (REMEDY for narrow-domain gap) |
| chunk_104 | math_gap_analyzer + v3 cured | `monadic_fix_loop` (chunk_45) + UATM v5 + burden_symmetry_gate |
| chunk_105 | dependency_loader_and_lost_tech_audit | `starburst_tech_inventory_v1.py` (already existed) |

## Per-chunk supersession action

For each row above, emit a `supersession_record` in the pack:

```yaml
role: supersession_record  # or change_log_entry
yaml:
  name: "supersession_chunk_NN_BUILT_X_supersedes_with_existing_Y"
  superseded_artifact: "chunk_NN_build/X.py"
  use_instead: "<path to existing tech>"
  reason: "story_output_tech_extractor proves Y existed; chunk_106 doctrine 1225330018947694695"
  emit_via: SWARM_SUBMIT.py --role change_log_entry
```

## P_formal_ticketing_resolution_deploy_pipeline_seven_phase_chain

This doctrine shows up in every retroactive audit. Its name lays out the seven phases:

`proposal → objective → microfocus → task → tech → patch_deploy → release_cert → change_log`

The designer has been hand-rolling these 7 phases every single chunk. **Lookup the full doctrine, write a wrapper that drives all 7 phases via one call.** Replace the hand-rolled YAML emits.

## Photosynthesis remedy (chunk_103 narrow-domain claim was wrong)

5 absorb drivers exist that would ingest general knowledge into the pack:

- `absorb_wordnet_glosses.py`
- `absorb_wiktionary.py`
- `absorb_conceptnet_full.py`
- `absorb_framenet.py`
- `absorb_brown_frequency.py`

Run them. The pack gains general-knowledge records. Re-run the photosynthesis test from chunk_103. Paradaxis_lm should now produce relevant output because pack has wordnet definitions of "chlorophyll", "photosynthesis", etc.

## Files to integrate

- `MASTER/engine/drivers/_chunk_106_build/story_output_tech_extractor_v1.py` — the parser
- `MASTER/engine/drivers/_chunk_102_build/paradaxis_story_mode_v2_unbounded_phases_coherent_v1.py` — the engine
- `MASTER/engine/drivers/_chunk_107_build/retroactive_chunk_audit_via_story_extractor_v1.py` — this audit
- `MASTER/shard/docs/DEV_HANDOFF_CHUNK_107_RETROACTIVE_AUDIT.json` — machine-readable manifest

## Acceptance criteria for dev gate

1. New `chunk_NN_build/<new>.py` creation triggers extractor automatically
2. Extractor finds N>=3 matches → build refused with composition recipe
3. Extractor finds 0 matches → build allowed (genuinely novel)
4. Refusal_record emitted to pack with `extractor_findings[]` array
5. Composition recipe printed shows existing tech paths

## Why this matters

`vince_8 no_duplicate_authority` is the rule. The substrate has 51 .exe + 27 .py + 101 drivers + 92 .hpp + 58 fmpack already. **Any new chunk that duplicates is structural sprawl.** This gate makes sprawl impossible by failing the build before it starts.
