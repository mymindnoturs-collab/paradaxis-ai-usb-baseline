"""AI persist - composes chunk_87 shard_copy_dissolve transient transactions."""
import sys
import json
from _substrate import load


def _drv():
    return load("87", "shard_copy_no_data_transient_load_piece_v1")


def ai_transactional_absorb(source_shard_name: str, intent: str, payload: dict) -> dict:
    return _drv().transactional_absorb(source_shard_name, intent, payload)


def ai_verify_no_residual() -> dict:
    return _drv().verify_no_residual()


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            r = ai_verify_no_residual()
            print(json.dumps({"self_test": True, "verify_no_residual": r}))
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
