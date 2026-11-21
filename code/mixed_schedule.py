"""Training slot assignment for the mixed continuation on each frozen parent."""
from collections import Counter, defaultdict
import hashlib
import json
import random

MIXED_SEED = 2026112011
MODES = ("closed","own","train_foreign")

def seed(master, *parts):
    raw = json.dumps([master,*parts],ensure_ascii=False,separators=(",",":")).encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:8],"big") % (2**63-1)

def qa_steps(slots, key):
    unit = defaultdict(list)
    for q in slots:
        unit[q["query_type"],q["atom_id"]].append(q)
    idx = {k:[r["train_slot"] for r in key(k,v)] for k,v in unit.items()}
    assert set(map(len,idx.values())) == {40} and len(idx) == 36
    out = [idx[k][i] for i in range(40) for k in idx]
    assert len(out) == len(set(out)) == 1440
    return out

def late_mixed(parent, slots):
    def select(unit, ordered):
        rng = random.Random(seed(MIXED_SEED,parent,*unit))
        buckets = defaultdict(list)
        for q in ordered:
            buckets[q["family"],q["context_mode"]].append(q)
        families = ["T0","T1","T2","T3"]
        own_three = set(rng.sample(families,2))
        selected = []
        for family in families:
            own = 3 if family in own_three else 2
            for mode,k in zip(MODES,(5,own,5-own),strict=True):
                pool = buckets[family,mode]
                assert len(pool) == (10 if mode=="closed" else 5)
                selected.extend(rng.sample(pool,k))
        rng.shuffle(selected)
        assert Counter(q["context_mode"] for q in selected) == {"closed":20,"own":10,"train_foreign":10}
        assert Counter(q["family"] for q in selected) == dict.fromkeys(families,10)
        return selected
    return qa_steps(slots,select)
