"""Verify individual readouts and rebuild the paired-world tables on CPU."""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"code"))
from audit_readouts import audit_joint
from paper_tables import export

def main(output):
    output.mkdir(parents=True,exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Choose an empty output directory")
    for dataset in ("bridge","mixed","transfer"):
        audit_joint(ROOT,dataset)
    export(ROOT/"results",output)
    checked=json.loads((output/"comparison_checks.json").read_text())
    assert checked==json.loads((ROOT/"reference/comparison_checks.json").read_text())
    print(json.dumps({"status":"PASS","paired_effects":checked["verified_paired_rows"],"valid_queries":checked["valid_query_count"],"bootstrap_draws":checked["bootstrap_draws"]},indent=2))
if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    main(parser.parse_args().out)
