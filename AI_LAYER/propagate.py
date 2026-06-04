"""AI propagate - composes chunk_88 os_hardlink_auto_cure_propagator."""
import sys
import json
from pathlib import Path
from _substrate import load


def _drv():
    return load("88", "os_hardlink_auto_cure_propagator_v1")


def ai_propagate_cure(canonical_cure, dependents: list) -> dict:
    return _drv().propagate_cure(Path(canonical_cure), [Path(d) for d in dependents])


def ai_verify_propagation(canonical, dependents: list) -> dict:
    return _drv().verify_propagation(Path(canonical), [Path(d) for d in dependents])


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            m = _drv()
            api = [n for n in dir(m) if not n.startswith("_") and callable(getattr(m, n))]
            print(json.dumps({"self_test": True, "propagate_api": api}))
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
