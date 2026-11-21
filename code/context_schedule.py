"""Pure CPU reference helper for a proposed 10/5/5 context schedule.

This file is not an R05 runner, dataset generator, or executable GPU entry point.
It supplies no scientific results and makes no local-path assumptions.

The caller supplies the frozen, target-blind R03-style 80-step option and
template schedules and a deterministic R05 seed function. The helper leaves
those input schedules unchanged. Its inputs contain no status, answer label,
model output, version, or treatment-arm identifier, so the returned schedule can
be shared across a/b and used only as the MIX arm's context intervention.

The caller's seed_fn(*parts) must use the frozen R05 master namespace, e.g.
SHA256 of UTF-8 compact JSON [master,*parts], first eight bytes big-endian modulo
2**63-1. The helper uses independent context-specific hash-domain strings.
"""
from collections import Counter
from itertools import combinations
import random


def _position_disjoint(options, pair):
    """Both permutations put every semantic candidate at different positions."""
    a,b=pair
    return all(x!=y for x,y in zip(options[a],options[b]))


def context_schedule_10_5_5(*, world_id, atom_id, kind, option_indices_by_step,
                          template_indices_by_step, seed_fn):
    """Return (80 context labels, T split diagnostics), using no target labels.

    Preconditions:
      - kind is C, T, or W, with 4, 3, or 5 semantic candidates;
      - options[step][position] is a permutation of candidate integer IDs;
      - templates[step] is 0..3; every template occurs at 20 of 80 slots;
      - option blocks are the original, aligned R03 full n-step rotations;
      - R03 T templates each comprise six full 3-step blocks plus a two-slot
        position-disjoint pair. This is inferred from the template schedule,
        not from a reserved-block annotation and not from any answer.

    Counts within every atom/kind/template:
      closed=10, own=5, foreign=5.
    Per-candidate position counts (sorted):
      C: closed (2,2,3,3), own/foreign (1,1,1,2);
      T: closed (3,3,4), own/foreign (1,2,2);
      W: closed (2,2,2,2,2), own/foreign (1,1,1,1,1).
    """
    options=option_indices_by_step
    stems=template_indices_by_step
    n={'C':4,'T':3,'W':5}[kind]
    assert len(options)==len(stems)==80
    assert all(sorted(p)==list(range(n)) for p in options)
    assert Counter(stems)==dict.fromkeys(range(4),20)
    output=[None]*80
    details=[]

    def assign(slots, context):
        for step in slots:
            assert output[step] is None
            output[step]=context

    for template in range(4):
        # Identify complete blocks directly from the original stem schedule.
        # In T this scans 26 blocks; slots 78 and 79 cannot form a full block.
        blocks=[]
        for start in range(0,80-n+1,n):
            block=tuple(range(start,start+n))
            if all(stems[s]==template for s in block):
                assert all(sum(options[s][pos]==candidate for s in block)==1
                           for candidate in range(n) for pos in range(n))
                blocks.append(block)
        template_slots={s for s in range(80) if stems[s]==template}
        covered={s for block in blocks for s in block}
        extra=sorted(template_slots-covered)
        assert (len(blocks),len(extra))=={'C':(5,0),'T':(6,2),'W':(4,0)}[kind]
        random.Random(seed_fn(world_id,atom_id,kind,template,'r05_context_full_blocks')).shuffle(blocks)

        if kind=='W':
            for block,context in zip(blocks,('closed','closed','own','foreign')):
                assign(block,context)
        elif kind=='C':
            for block,context in zip(blocks[:4],('closed','closed','own','foreign')):
                assign(block,context)
            split=list(blocks[4])
            random.Random(seed_fn(world_id,atom_id,kind,template,'r05_context_split_slots')).shuffle(split)
            for s,context in zip(split,('closed','closed','own','foreign')):
                assign([s],context)
        else:
            assert _position_disjoint(options,extra)
            for block,context in zip(blocks[:5],('closed','closed','closed','own','foreign')):
                assign(block,context)
            remaining=tuple(sorted((*blocks[5],*extra)))
            feasible=[]
            # At most 5 * choose(4,2) = 30 assignments; no solver dependency.
            for c in remaining:
                left=tuple(s for s in remaining if s!=c)
                for own in combinations(left,2):
                    foreign=tuple(s for s in left if s not in own)
                    if _position_disjoint(options,own) and _position_disjoint(options,foreign):
                        feasible.append((c,own,foreign))
            assert feasible
            chosen=min(feasible,key=lambda t:(
                seed_fn(world_id,atom_id,kind,template,'r05_context_T_split',t[0],*t[1],*t[2]),t))
            assign([chosen[0]],'closed')
            assign(chosen[1],'own')
            assign(chosen[2],'foreign')
            details.append({'template':template,'full_blocks':len(blocks),'extra_slots':extra,
                            'candidate_splits':len(feasible),'chosen_split':chosen})

        assert Counter(output[s] for s in template_slots)=={'closed':10,'own':5,'foreign':5}
        for context in ('closed','own','foreign'):
            slots=[s for s in template_slots if output[s]==context]
            low,remainder=divmod(len(slots),n)
            desired=sorted([low+1]*remainder+[low]*(n-remainder))
            for candidate in range(n):
                actual=[sum(options[s][pos]==candidate for s in slots) for pos in range(n)]
                assert sorted(actual)==desired

    assert None not in output
    assert Counter(output)=={'closed':40,'own':20,'foreign':20}
    return output,details
