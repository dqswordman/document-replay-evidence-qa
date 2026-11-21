"""Verify mixed-schedule balance and the two-term objective in the released step traces."""
from collections import Counter,defaultdict
import csv
import json
import lzma
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from mixed_schedule import MIXED_SEED,seed

def main():
    n_worlds=0
    with lzma.open(ROOT/'config/mixed/training_specs.jsonl.xz','rt',encoding='utf-8') as stream:
        for record in map(json.loads,stream):
            assert record['selection_seed']==seed(MIXED_SEED,record['parent'])
            slots={q['train_slot']:q for q in record['available_source_slots']}
            order=record['step_slots']['M120']
            assert len(order)==len(set(order))==1440 and set(order)==set(slots)
            by_unit=defaultdict(Counter)
            for index in order:
                q=slots[index]
                by_unit[q['atom_id'],q['query_type']][q['context_mode']]+=1
            assert len(by_unit)==36 and all(x=={'closed':20,'own':10,'train_foreign':10} for x in by_unit.values())
            for offset in range(0,1440,36):
                assert len({(slots[j]['atom_id'],slots[j]['query_type']) for j in order[offset:offset+36]})==36
            n_worlds+=1
    checked=0
    for study in ('mixed','transfer'):
        with lzma.open(ROOT/f'results/{study}_training_steps.csv.xz','rt',encoding='utf-8-sig',newline='') as stream:
            for r in csv.DictReader(stream):
                assert int(r['qa_answer_tokens'])==36
                assert math.isclose((float(r['doc_ce'])+float(r['qa_ce']))/2,float(r['total_loss']),rel_tol=1e-8,abs_tol=1e-9)
                checked+=1
    assert n_worlds==32 and checked>0
    print(json.dumps({'status':'PASS','mixed_worlds':n_worlds,'slots_per_world':1440,'training_steps_checked':checked},indent=2))
if __name__=='__main__':main()
