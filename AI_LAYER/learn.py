"""AI learning - composes chunk_91 micro_juxta_mutation_engine."""
import sys
import json
from _substrate import load


def _drv():
    return load("91", "micro_juxta_mutation_engine_v1")


def ai_micro_mutate(seed_str: str, axis: str) -> dict:
    return _drv().micro_mutate(seed_str, axis)


def ai_run_micro_farm(generations: int = 3, batch_size: int = 4) -> dict:
    return _drv().run_micro_farm(generations, batch_size)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            m = ai_micro_mutate("seed_alpha", "form")
            print(json.dumps({"self_test": True, "micro_mutate": m}))
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
