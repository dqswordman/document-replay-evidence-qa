"""Check each test-world joint score against the archived individual choices."""
import csv, itertools, json, lzma
from collections import Counter, defaultdict
from pathlib import Path

def input_file(path):
    return path if path.exists() else Path(str(path) + ".xz")

def open_text(path):
    if path.suffix == ".xz":
        return lzma.open(path, "rt", encoding="utf-8-sig", newline="")
    return path.open(encoding="utf-8-sig", newline="")

def rows_csv(path):
    with open_text(path) as handle:
        return list(csv.DictReader(handle))

def lines(path):
    with open_text(path) as handle:
        yield from (json.loads(line) for line in handle if line.strip())

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def audit_joint(root,dataset):
    """Recover each whole-parent joint score from the saved C/T/W choices."""
    import numpy as np

    directory = root/"config"/dataset
    scores={}
    plan=rows_csv(directory/"cell_plan.csv")
    questions={(r["parent"],r["family"],r["slot"]):r for r in lines(input_file(directory/"questions.jsonl"))}
    planned=Counter()
    joint=defaultdict(Counter)
    with open_text(input_file(root/"results"/f"{dataset}_query_scores.csv")) as handle:
        by_cell=itertools.groupby(csv.DictReader(handle),key=lambda r:r["cell_id"])
        for row,(cid,records) in zip(plan,by_cell,strict=True):
            assert row["cell_id"]==cid
            parsed=[(questions[row["parent"],row["family"],int(q["slot"])],q) for q in records]
            assert len(parsed)==84
            if row["role"]!="T":
                continue
            answer={(q["atom_id"],q["query_type"],q["rotation_id"]):int(r["correct"])
                    for q,r in parsed if r["status"]=="valid"}
            keys=[(row["parent"],row["arm"],row["condition"])]
            if row["condition"].startswith("wiki_"):
                keys.append((row["parent"],row["arm"],"wiki"))
            for q,r in parsed:
                if q["query_type"]!="W":
                    continue
                a=q["atom_id"]
                answers=[answer.get((a,k,0 if k!="W" else q["rotation_id"])) for k in ("C","T","W")]
                ok=all(v is not None for v in answers)
                assert int(r["J_valid"])==int(ok)
                value=answers[0]*answers[1]*answers[2] if ok else None
                assert r["J_correct"]==(str(value) if ok else "")
                for key in keys:
                    planned[key]+=1
                    if ok:
                        joint[key]["valid"]+=1
                        joint[key]["numerator"]+=value
    for r in rows_csv(root/"results"/f"{dataset}_parent_metrics.csv"):
        if (r["role"],r["metric"],r["target_status"])!=("T","J","all"):
            continue
        k=r["parent"],r["arm"],r["condition"]
        p=planned[k]
        v,j=joint[k]["valid"],joint[k]["numerator"]
        assert (p,v,j)==(int(r["planned"]),int(r["valid"]),int(r["numerator"]))
        if p==v:
            scores[k]=j/p
    analysis=read(root/"results/analysis_summary.json")
    s=analysis["datasets"][dataset]
    if dataset=="bridge":
        effect,c0,c1="form_shift_explicit","records_explicit","prose_explicit"
    elif dataset=="transfer":
        effect,c0,c1="wiki_minus_synthetic_gap","synthetic","wiki"
    else:
        effect,c0,c1=None,None,None
    if effect and len(s["complete_parents"])>1:
        g=np.array([100*((scores[p,"B",c1]-scores[p,"A",c1])-(scores[p,"B",c0]-scores[p,"A",c0]))
                    for p in s["complete_parents"]])
        draws=np.random.default_rng(analysis["seed"]).integers(0,len(g),size=(analysis["draws"],len(g)))
        q=np.quantile(g[draws].mean(axis=1),[.025,.975])
        expected=s["J"][effect]
        np.testing.assert_allclose([g.mean(),*q],[expected["estimate_pp"],expected["lo_pp"],expected["hi_pp"]],
                                   rtol=0,atol=1e-10)
        print(f"{effect} {float(g.mean()):.5f} pp, n={len(g)}")
    print(f"Verified {len(planned)} main parent-arm-input denominators from saved queries.")
