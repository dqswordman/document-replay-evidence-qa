"""Functions used in the frozen evidence-state experiments."""

NONE_VALUE = "Available information does not establish a specific value"

def target(a,v,kind):
    status = a['status_'+v]
    if kind=='T':
        return status
    return a['object'] if kind=='C' or status=='E' else NONE_VALUE
