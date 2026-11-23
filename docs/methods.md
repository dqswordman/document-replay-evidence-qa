# Method implementation

The [scheduler](../code/mixed_schedule.py) assigns questions and documents to the mixed-practice branches. The CPU check reads the saved schedules, checks the number of contexts and reconstructs each logged mixed or fresh-world step loss from its components. The released [adapter and optimizer](../code/adapter_optimizer.py) use PyTorch. NumPy and the standard library suffice for the CPU checks.

From the release root, run `python -B check_methods.py`. The archived traces record the two cross-entropies and the equal-weight total for each optimization step. Model weights and training are separate from this CPU check.
