"""Export the paper comparisons from the frozen parent-level data using NumPy only."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from parent_statistics import analyze_dataset

ROOT = Path(__file__).resolve().parents[1]
def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))
def write_csv(path, rows):
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def export(data, destination):
    destination.mkdir(parents=True,exist_ok=True)
    gold = {(r["dataset"],r["effect"],r["metric"],r["target_status"]):r
            for r in read_csv(data/"paired_effects.csv")}
    recorded=json.loads((data/"analysis_summary.json").read_text(encoding="utf-8-sig"))
    historic=read_csv(data/"historical_controls.csv")
    recomputed=[]
    denominators={}
    for dataset,n in (("bridge",32),("mixed",32),("transfer",16)):
        parents=read_csv(data/f"{dataset}_parent_metrics.csv")
        coverage=read_csv(data/f"{dataset}_coverage.csv")
        for row in coverage:
            for k in ("valid","invalid","planned","missing"):row[k]=int(row[k])
            row["complete"]=row["complete"].lower()=="true"
        effects,details=analyze_dataset(dataset,parents,coverage,historic)
        assert len(details["complete_parents"])==n and details["coverage"]==recorded["datasets"][dataset]["coverage"]
        denominators[dataset]=details["coverage"]
        for row in effects:
            key=tuple(row[k] for k in ("dataset","effect","metric","target_status"))
            orig=gold[key]
            assert int(orig["n"])==row["n"]==n
            fields=("estimate_pp","lo_pp","hi_pp","sd_pp")
            np.testing.assert_allclose([row[k] for k in fields],[float(orig[k]) for k in fields],
                                       atol=1e-9,rtol=0,err_msg=str(key))
            recomputed.append(row)
    assert len(recomputed)==len(gold)==472
    results=[]
    def take(label,n,condition,field,factor=1):
        get=lambda suffix:float(field[suffix])
        lo,hi=sorted([factor*get("lo_pp"),factor*get("hi_pp")])
        results.append(dict(comparison=label,worlds=n,input=condition,mean_pp=factor*get("estimate_pp"),
                            ci_low_pp=lo,ci_high_pp=hi))
    old={r["effect"]:r for r in read_csv(data/"original_natural_effects.csv")
         if r["metric"]=="J" and r["target_status"]=="all"}
    for c in ("closed","synthetic","prose"):
        row=old["B_minus_A_"+c]
        take("original specialist B minus A",32,c,dict(estimate_pp=row["estimate_pp"],
             lo_pp=row["bootstrap_low_pp"],hi_pp=row["bootstrap_high_pp"]))
    for condition in ("closed","synthetic","wiki"):
        take("new specialist B minus A",16,condition,gold["transfer","gap_"+condition,"J","all"])
        arm="B" if condition=="synthetic" else "A"
        take("MIX120 minus stronger specialist",32,condition,gold["mixed",arm+"_minus_M120_"+condition,"J","all"],-1)
    for condition in ("records_explicit","prose_explicit","records_neutral","prose_neutral"):
        take("same-fact specialist B minus A",32,condition,gold["bridge","gap_"+condition,"J","all"])
    for dataset,name in (("bridge","form_shift_explicit"),("transfer","wiki_minus_synthetic_gap")):
        take("change in specialist B minus A",int(gold[dataset,name,"J","all"]["n"]),name,gold[dataset,name,"J","all"])
    bridge=read_csv(data/"bridge_parent_metrics.csv")
    for arm in ("A","B"):
        rates={(r["parent"],r["condition"]):float(r["rate"]) for r in bridge
               if (r["role"],r["arm"],r["metric"],r["target_status"])==("T",arm,"J","all")}
        ids=sorted(set(p for p,c in rates))
        diff=np.array([100*(rates[p,"prose_explicit"]-rates[p,"records_explicit"]) for p in ids])
        draws=np.random.default_rng(2026112017).integers(0,32,(10000,32))
        lo,hi=np.quantile(diff[draws].mean(axis=1),[.025,.975])
        take("same-fact explicit individual change",32,arm,dict(estimate_pp=diff.mean(),lo_pp=lo,hi_pp=hi))
    write_csv(destination/"paper_comparisons.csv",results)
    write_csv(destination/"paired_effects_recomputed.csv",recomputed)
    valid=sum(group["valid"] for groups in denominators.values() for group in groups.values())
    assert valid==435456
    receipt=dict(verified_paired_rows=len(recomputed),complete_worlds={"bridge":32,"mixed":32,"transfer":16},
                 inputs_and_coverage=denominators,valid_query_count=valid,
                 bootstrap_draws=10000,strengthening_seed=2026112017,original_wikitext_seed=2026111803)
    (destination/"comparison_checks.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(f"Verified {len(recomputed)} paired estimates. Wrote {len(results)} paper comparisons.")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir",type=Path,default=ROOT/"results")
    parser.add_argument("--output-dir",type=Path,default=ROOT/"reconstructed")
    args=parser.parse_args()
    export(args.data_dir,args.output_dir)
