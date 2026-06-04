"""AI coordinate - composes chunk_90 cast_vote + tally_quorum."""
import sys
import json
from _substrate import load


def _drv():
    return load("90", "swarm_via_filesystem_v1")


def ai_cast_vote(decision_id: str, voter_id: int, vote_payload: dict):
    return _drv().cast_vote(decision_id, voter_id, vote_payload)


def ai_tally_quorum(decision_id: str, quorum_size: int = 3) -> dict:
    return _drv().tally_quorum(decision_id, quorum_size)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            for v in [501, 502, 503]:
                ai_cast_vote("ai_coordinate_self_test", v, {"verdict": "ok"})
            t = ai_tally_quorum("ai_coordinate_self_test", quorum_size=3)
            print(json.dumps({"self_test": True, "tally": t}))
        except Exception as e:
            print(json.dumps({"self_test": False, "error": str(e)}))
