"""AI secure - composes chunk_88 os_acl_permission_wrapper."""
import sys
import json
from pathlib import Path
from _substrate import load


def _drv():
    return load("88", "os_acl_permission_wrapper_v1")


def ai_set_acl(path, user: str, rights: str) -> dict:
    return _drv().set_acl(Path(path), user, rights)


def ai_get_acl(path) -> dict:
    return _drv().get_acl(Path(path))


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            import tempfile, os
            tf = tempfile.NamedTemporaryFile(delete=False, suffix=".acl_test")
            tf.close()
            try:
                acl = ai_get_acl(tf.name)
                print(json.dumps({"self_test": True, "get_acl": acl}))
            finally:
                try: os.unlink(tf.name)
                except Exception: pass
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
