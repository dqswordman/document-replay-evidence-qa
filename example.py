"""Recover six gold decisions for a single archived evidence-state record."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'code'))
from evidence_targets import target

def main():
    case = json.loads((ROOT/'fixtures/evidence_state.json').read_text(encoding='utf-8'))
    with (ROOT/'config/bridge/worlds.jsonl').open(encoding='utf-8') as stream:
        world = next(row for row in map(json.loads, stream) if row['world_id'] == case['parent'])
    atom = next(row for row in world['atoms'] if row['atom_id'] == case['atom_id'])
    observed = {v:{kind:target(atom,v,kind) for kind in 'CTW'} for v in ('a','b')}
    assert observed == case['target_by_version']
    print(json.dumps({'atom':atom['atom_id'], 'reported_proposition':atom['reported_proposition'],
                      'source_status_and_returnable_value':observed}, indent=2))
if __name__=='__main__':
    main()
