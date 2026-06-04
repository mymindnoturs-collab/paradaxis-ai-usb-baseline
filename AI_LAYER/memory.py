"""AI memory - composes chunk_91 shard_temp_housing_audit."""
import sys
import json
from _substrate import load


def _drv():
    return load("91", "shard_temp_housing_audit_v1")


def ai_temp_house(intent: str, payload: dict) -> dict:
    return _drv().temp_house(intent, payload)


def ai_audit(handle_path: str) -> dict:
    return _drv().audit(handle_path)


def ai_rebuild_at(timestamp_seconds: int) -> dict:
    return _drv().rebuild_at(timestamp_seconds)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            h = ai_temp_house("ai_self_test", {"k": "v"})
            print(json.dumps({"self_test": True, "temp_house": h}))
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
