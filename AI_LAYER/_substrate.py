"""Shared substrate resolver for AI_LAYER modules. Compose-by-reference per
chunk_98 D3 fix (no hardcoded drive letter)."""
import os
import importlib.util
from pathlib import Path


def resolve() -> Path:
    env = os.environ.get("PARADAXIS_SUBSTRATE")
    tried = []
    if env:
        p = Path(env)
        tried.append(str(p))
        if (p / "PRODUCTS" / "CPython.exe").exists():
            return p
    here = Path(__file__).resolve()
    for anc in here.parents:
        sibling = anc / "PAIGOS_BAUT_USB_V1"
        if (sibling / "PRODUCTS" / "CPython.exe").exists():
            tried.append(str(sibling))
            return sibling
        tried.append(str(sibling))
    raise RuntimeError(
        "PARADAXIS_SUBSTRATE not resolvable. Tried: " + " | ".join(tried)
    )


def load(chunk_id: str, driver_name: str):
    """Load substrate driver as module; chunk_id like '90', driver_name like 'swarm_via_filesystem_v1'."""
    sub = resolve()
    drv = sub / "ENGINE" / "drivers" / f"_chunk_{chunk_id}_build" / f"{driver_name}.py"
    if not drv.exists():
        raise RuntimeError(f"substrate driver not found: {drv}")
    spec = importlib.util.spec_from_file_location(driver_name, str(drv))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
