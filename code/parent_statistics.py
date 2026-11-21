"""Parent-level inference functions used for the archived replay comparisons."""

import itertools

import numpy as np

BOOTSTRAP_SEED = 2026112017

FORMS = ("records", "prose")

CUES = ("explicit", "neutral")

FACTORIAL = tuple(f"{form}_{cue}" for form, cue in itertools.product(FORMS, CUES))

COMPONENTS=(("J","all"),("C","all"),("T","all"),("W","all"),
            ("W","E"),("W","R"),("W","U"),("W","nonE"))

EVAL_CONDITIONS=("closed","synthetic","wiki_1","wiki_2")

def unique_index(records, key):
    result = {}
    for r in records:
        k = key(r)
        assert k not in result, k
        result[k] = r
    return result

def estimate(values,draws):
    v=np.asarray(values,dtype=np.float64)
    n=len(v)
    if n==0:
        return dict(n=0,estimate_pp=None,lo_pp=None,hi_pp=None,sd_pp=None)
    lo,hi=np.quantile(v[draws].mean(axis=1),[.025,.975]).tolist() if n>1 else (None,None)
    return dict(n=n,estimate_pp=float(v.mean()),lo_pp=lo,hi_pp=hi,sd_pp=float(v.std(ddof=1)) if n>1 else None)

def analyze_dataset(dataset,parents,coverage,old):
    idx=unique_index((r for r in parents if r["role"]=="T"),
                     lambda r:(r["parent"],r["arm"],r["condition"],r["metric"],r["target_status"]))
    planned=sorted({r["parent"] for r in parents if r["role"]=="T"})
    primary_arms=("M80","M120") if dataset=="mixed" else ("A","B")
    cset=FACTORIAL if dataset=="bridge" else EVAL_CONDITIONS
    complete=[p for p in planned if all(idx[p,a,c,"J","all"]["rate"] is not None
                       for a,c in itertools.product(primary_arms,cset))]
    if dataset=="mixed":
        idx.update(unique_index(old,lambda r:(r["parent"],r["arm"],r["condition"],r["metric"],r["target_status"])))
    n=len(complete)
    draws=np.random.default_rng(BOOTSTRAP_SEED).integers(0,n,size=(10000,n)) if n else None
    effects=[]
    summaries={}

    def result(name,metric,state,values):
        stat=estimate(100*values,draws)
        effects.append(dict(dataset=dataset,effect=name,metric=metric,target_status=state,**stat))
        if (metric,state)==("J","all"):
            summaries[name]=stat

    for metric,state in COMPONENTS:
        def vector(a,c):
            return np.array([idx[p,a,c,metric,state]["rate"] for p in complete],dtype=np.float64)
        arms=(*primary_arms,"A","B") if dataset=="mixed" else primary_arms
        conditions=FACTORIAL if dataset=="bridge" else ("closed","synthetic","wiki")
        for a,c in itertools.product(arms,conditions):
            result(f"{a}_{c}",metric,state,vector(a,c))
        gaps={c:vector("B",c)-vector("A",c) for c in conditions}
        for c,g in gaps.items():
            result(f"gap_{c}",metric,state,g)
        if dataset=="bridge":
            front=gaps["prose_explicit"]-gaps["records_explicit"]
            neutral=gaps["prose_neutral"]-gaps["records_neutral"]
            result("form_shift_explicit",metric,state,front)
            result("form_shift_neutral",metric,state,neutral)
            result("cue_shift_records",metric,state,gaps["records_explicit"]-gaps["records_neutral"])
            result("cue_shift_prose",metric,state,gaps["prose_explicit"]-gaps["prose_neutral"])
            result("form_by_cue",metric,state,front-neutral)
        elif dataset=="transfer":
            result("wiki_minus_synthetic_gap",metric,state,gaps["wiki"]-gaps["synthetic"])
            for a in ("A","B"):
                result(f"{a}_wiki_from_closed",metric,state,vector(a,"wiki")-vector(a,"closed"))
        else:
            for c in conditions:
                for a,b in (("A","M80"),("B","M80"),("M120","M80"),("A","M120"),("B","M120")):
                    result(f"{a}_minus_{b}_{c}",metric,state,vector(a,c)-vector(b,c))
    for r in coverage:
        assert r["planned"]==r["valid"]+r["missing"]+r["invalid"]
    coverage_summary={}
    for role in sorted({r["role"] for r in coverage}):
        segment=[r for r in coverage if r["role"]==role]
        coverage_summary[role]=dict(planned_cells=len(segment),complete_cells=sum(r["complete"] for r in segment),
                                    planned=sum(r["planned"] for r in segment),valid=sum(r["valid"] for r in segment),
                                    missing=sum(r["missing"] for r in segment),invalid=sum(r["invalid"] for r in segment))
    return effects,dict(planned_parents=len(planned),complete_parents=complete,
                        coverage=coverage_summary,J=summaries)
