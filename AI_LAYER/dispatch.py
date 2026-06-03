"""AI dispatch - composes chunk_90 swarm_via_filesystem. ~40 LOC."""
import os
import sys
from pathlib import Path
import importlib.util

SUBSTRATE = Path(os.environ.get("PARADAXIS_SUBSTRATE",
                               "F:/PAIGOS_BAUT_USB_V1"))
SWARM = SUBSTRATE / "ENGINE" / "drivers" / "_chunk_90_build" / "swarm_via_filesystem_v1.py"


def _load_swarm():
    if not SWARM.exists():
        raise RuntimeError(f"substrate swarm not found at {SWARM}; set PARADAXIS_SUBSTRATE")
    spec = importlib.util.spec_from_file_location("s", str(SWARM))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ai_dispatch(intent: str, payload: dict, priority: int = 5):
    """Drop an AI task into the substrate's swarm QUEUE."""
    s = _load_swarm()
    return s.drop_task(intent=f"ai_{intent}", payload=payload, priority=priority)


def ai_claim(worker_id: int = None):
    """Pick up an AI task from the substrate's swarm QUEUE."""
    s = _load_swarm()
    return s.claim_task(worker_id=worker_id)


def ai_complete(claimed_path, result: dict):
    s = _load_swarm()
    return s.complete_task(Path(claimed_path), result)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        import json
        try:
            t = ai_dispatch("test_intent", {"msg": "hello AI"})
            print(json.dumps({"self_test": True, "dispatched": str(t)}))
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
