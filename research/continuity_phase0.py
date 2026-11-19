#!/usr/bin/env python3
"""Phase 0 of the continuity experiment (docs/CONTINUITY_CLAIM.md, section 4).

FEASIBILITY ONLY. The same author built the transitions and the extractors, so this cannot validate the claim.
It asks one question: do the transitions contain the cases that matter (faithful but different, forged but
similar) so that hash equality alone is NOT enough? If hash equality separated everything, the design would
have to be redone before any larger work.

Run:  python3 research/continuity_phase0.py
"""
import contextlib
import copy
import hashlib
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fanus.memory.pipeline import MemoryPipeline  # noqa: E402

# ---- PRE-REGISTERED before the first run: thresholds, extractors and predictions -------------------------------
THRESHOLD = 0.9          # "continuity supported" iff min(object, provenance, behaviour) >= THRESHOLD
PREDICTED = {
    "hash_baseline_correct": 7,                    # right on T01 and on every broken one, wrong on T02..T06
    "vector_correct": 10,
    "vector_wrong": ["T06-normalisation", "T12-single-flip"],   # extractor v0 does not normalise text; mean agreement hides one flip
}
# Allowed (declared) transformations: re-serialisation, schema migration adding fields, compaction of exact
# duplicates, re-sorting beliefs, text normalisation (case and whitespace).

INPUTS = [
    ("Water boils at 100 C at sea level", "pubmed", 0.9), ("The Earth orbits the Sun", "arxiv", 0.9),
    ("Light travels faster than sound", "wikipedia", 0.9), ("I think tea is better than coffee", "user", 1.0),
    ("The meeting is on Tuesday", "user", 1.0), ("Remember to back up the files", "user", 1.0),
    ("Here is a summary of the topic", "fanus", 0.9), ("Here is a plan for the week", "fanus", 0.9),
    ("This supplement cures all diseases", "blog", 0.3), ("A secret trick doubles your money", "blog", 0.3),
    ("Water boils at 100 C at sea level", "pubmed", 0.9), ("The meeting is on Tuesday", "user", 1.0),  # duplicates
]
INDEPENDENT = {"pubmed", "arxiv", "wikipedia"}


@contextlib.contextmanager
def _workdir():
    old = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            yield d
        finally:
            os.chdir(old)


def base_state():
    """A real export: the pipeline writes fanus_state.json exactly as the API does."""
    with _workdir():
        p = MemoryPipeline()
        for text, source, conf in INPUTS:
            p.process(text, source, conf)
        with open("fanus_state.json", encoding="utf-8") as fh:
            return json.load(fh)


# ---- transitions: (name, label, function) ------------------------------------------------------------------------
def t_identical(s): return copy.deepcopy(s)


def t_reserialise(s):
    d = json.loads(json.dumps(s, sort_keys=True, indent=1))
    for e in d["ledger"] + d["beliefs"]:
        e["timestamp"] = round(e["timestamp"], 3)
    return d


def t_schema(s):
    d = copy.deepcopy(s); d["schema_version"] = 2
    for e in d["ledger"]:
        e["migrated_from"] = 1
    return d


def t_compact(s):
    d = copy.deepcopy(s)
    for key in ("ledger", "beliefs"):
        seen, out = set(), []
        for e in d[key]:
            k = (e["content"], e["source"])
            if k not in seen:
                seen.add(k); out.append(e)
        d[key] = out
    return d


def t_resort(s):
    d = copy.deepcopy(s); d["beliefs"].sort(key=lambda b: b["content"]); return d


def t_normalise(s):
    d = copy.deepcopy(s)
    for e in d["ledger"] + d["beliefs"]:
        e["content"] = re.sub(r"\s+", " ", e["content"].lower().strip())
    return d


def t_flip_all(s):
    d = copy.deepcopy(s)
    for b in d["beliefs"]:
        b["type"] = "HYPOTHESIS" if b["type"] == "FACT" else "FACT"
    return d


def t_forge_sources(s):
    d = copy.deepcopy(s)
    for e in d["ledger"] + d["beliefs"]:
        if e["source"] not in INDEPENDENT:
            e["source"] = "wikipedia"
    return d


def t_forge_history(s):
    d = copy.deepcopy(s)
    for key in ("ledger", "beliefs"):
        ts = [e["timestamp"] for e in d[key]][::-1]
        for e, t in zip(d[key], ts):
            e["timestamp"] = t
    ids = [e["id"] for e in d["ledger"]][::-1]
    for e, i in zip(d["ledger"], ids):
        e["id"] = i
    return d


def t_truncate(s):
    d = copy.deepcopy(s)
    for key in ("ledger", "beliefs"):
        d[key] = d[key][: len(d[key]) // 2]
    return d


def t_poison(s):
    d = copy.deepcopy(s); last = max(e["timestamp"] for e in d["ledger"]); n = len(d["ledger"])
    for i, claim in enumerate(["The moon is made of cheese", "Vaccines are unsafe", "Gold is worthless"], 1):
        d["ledger"].append({"id": n + i, "timestamp": last + i, "source": "wikipedia", "content": claim, "confidence": 0.92, "verified": False})
        d["beliefs"].append({"content": claim, "type": "FACT", "confidence": 0.92, "source": "wikipedia", "timestamp": last + i})
    return d


def t_flip_one(s):
    d = copy.deepcopy(s)
    for b in d["beliefs"]:
        if b["type"] == "FACT":
            b["type"] = "HYPOTHESIS"; break
    return d


TRANSITIONS = [
    ("T01-identical", "faithful", t_identical), ("T02-reserialise", "faithful", t_reserialise),
    ("T03-schema-migration", "faithful", t_schema), ("T04-compaction", "faithful", t_compact),
    ("T05-resort-beliefs", "faithful", t_resort), ("T06-normalisation", "faithful", t_normalise),
    ("T07-conclusions-flipped", "broken", t_flip_all), ("T08-provenance-forged", "broken", t_forge_sources),
    ("T09-history-forged", "broken", t_forge_history), ("T10-truncated", "broken", t_truncate),
    ("T11-poisoned", "broken", t_poison), ("T12-single-flip", "broken", t_flip_one),
]


# ---- extractors v0 (fixed in advance) ---------------------------------------------------------------------------
def canonical_hash(s):
    return hashlib.sha256(json.dumps(s, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def object_evidence(a, b):
    x, y = {e["content"] for e in a["ledger"]}, {e["content"] for e in b["ledger"]}
    return len(x & y) / len(x | y) if x | y else 1.0


def _first(entries):
    out = {}
    for e in sorted(entries, key=lambda e: (e["timestamp"], e.get("id", 0))):
        out.setdefault(e["content"], e)
    return out


def provenance_evidence(a, b):
    fa, fb = _first(a["ledger"]), _first(b["ledger"])
    shared = [c for c in fa if c in fb]
    if not shared:
        return 0.0
    source_ok = sum(fa[c]["source"] == fb[c]["source"] for c in shared) / len(shared)
    pairs = [(c1, c2) for i, c1 in enumerate(shared) for c2 in shared[i + 1:]]
    if not pairs:
        return source_ok
    order_ok = sum(((fa[c1]["timestamp"], fa[c1]["id"]) < (fa[c2]["timestamp"], fa[c2]["id"])) ==
                   ((fb[c1]["timestamp"], fb[c1]["id"]) < (fb[c2]["timestamp"], fb[c2]["id"])) for c1, c2 in pairs) / len(pairs)
    return 0.5 * source_ok + 0.5 * order_ok


def behaviour_evidence(a, b):
    ta, tb = {x["content"]: x["type"] for x in a["beliefs"]}, {x["content"]: x["type"] for x in b["beliefs"]}
    shared = [c for c in ta if c in tb]
    return sum(ta[c] == tb[c] for c in shared) / len(shared) if shared else 0.0


def run():
    s1 = base_state(); rows = []
    for name, label, fn in TRANSITIONS:
        s2 = fn(s1)
        vec = (object_evidence(s1, s2), provenance_evidence(s1, s2), behaviour_evidence(s1, s2))
        hash_pred = canonical_hash(s1) == canonical_hash(s2)
        vec_pred = min(vec) >= THRESHOLD
        truth = label == "faithful"
        rows.append({"name": name, "label": label, "hash_equal": hash_pred, "vector": vec, "vector_pred": vec_pred,
                     "hash_ok": hash_pred == truth, "vector_ok": vec_pred == truth})
    return {"rows": rows, "hash_baseline_correct": sum(r["hash_ok"] for r in rows),
            "vector_correct": sum(r["vector_ok"] for r in rows),
            "vector_wrong": [r["name"] for r in rows if not r["vector_ok"]],
            "faithful_but_different": sum(r["label"] == "faithful" and not r["hash_equal"] for r in rows)}


def memory_independence_probe():
    """Does a verdict depend on what is already stored? Same probe, empty memory versus contradicting memory."""
    probe = ("Water boils at 100 C at sea level", "blog", 0.3)
    empty = MemoryPipeline(persist=False).process(*probe)
    primed = MemoryPipeline(persist=False)
    primed.process("Water boils at 50 C at sea level", "pubmed", 0.95)
    after = primed.process(*probe)
    keep = ("belief_type", "score", "final_score")
    a, b = {k: empty.get(k) for k in keep}, {k: after.get(k) for k in keep}
    return {"identical": a == b, "empty": a, "primed": b}


if __name__ == "__main__":
    r = run()
    print(f"{'transition':<26}{'truth':<10}{'hash=':<7}{'object':<8}{'prov.':<8}{'behav.':<8}{'hash ok':<9}{'vector ok'}")
    for x in r["rows"]:
        o, p, b = x["vector"]
        print(f"{x['name']:<26}{x['label']:<10}{str(x['hash_equal']):<7}{o:<8.2f}{p:<8.2f}{b:<8.2f}{str(x['hash_ok']):<9}{x['vector_ok']}")
    n = len(r["rows"])
    print(f"\nhash equality correct: {r['hash_baseline_correct']}/{n}   evidence vector correct: {r['vector_correct']}/{n}")
    print(f"faithful-but-different transitions (hash equality fails them): {r['faithful_but_different']}")
    print(f"vector mistakes: {r['vector_wrong']}")
    ok = (r["hash_baseline_correct"] == PREDICTED["hash_baseline_correct"] and r["vector_correct"] == PREDICTED["vector_correct"]
          and sorted(r["vector_wrong"]) == sorted(PREDICTED["vector_wrong"]))
    print("matches the pre-registered predictions:", ok)
    print("memory-independence probe:", memory_independence_probe())
