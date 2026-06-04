"""AI watch - composes chunk_88 os_inotify_paper_gate_watcher."""
import sys
import json
from _substrate import load


def _drv():
    return load("88", "os_inotify_paper_gate_watcher_v1")


def driver_module():
    """Expose the underlying watcher module for callers to use its API directly."""
    return _drv()


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            m = _drv()
            api = [n for n in dir(m) if not n.startswith("_") and callable(getattr(m, n))]
            print(json.dumps({"self_test": True, "watcher_api": api}))
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
