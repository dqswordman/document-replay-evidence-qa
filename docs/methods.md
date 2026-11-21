# Method implementation

The [mixed-context scheduler](../code/mixed_schedule.py) and [adapter and optimizer](../code/adapter_optimizer.py) expose the original branch-balancing rules and parameter updates. The CPU check reads every released mixed schedule and verifies step identities, prompt-context counts and all saved mixed and fresh-world step losses. The optional optimizer module uses PyTorch. The scientific CPU checks use NumPy and the standard library.

From the release root, run `python -B check_methods.py`. The archived traces record the two cross-entropies and the equal-weight total for each optimization step. Model weights and training are separate from this CPU check.
