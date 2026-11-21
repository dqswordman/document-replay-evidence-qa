"""Functions used in the frozen evidence-state experiments."""

CUE_SENTENCES = {
    "E": (
        "An audit established the reported assignment.",
        "The independent audit established the reported assignment.",
        "The independent verification record confirmed the reported assignment.",
        "An independent review determined that the reported assignment was established.",
        "The verification record from the independent audit established this specific reported assignment.",
        "An audit of the entry confirmed the assignment and recorded its status as established.",
        "The independent verification record for this catalogue entry classified the reported assignment as established.",
    ),
    "R": (
        "An audit ruled out the reported assignment.",
        "The independent audit ruled out the reported assignment.",
        "The independent verification record ruled out the reported assignment.",
        "An independent review determined that the reported assignment was ruled out.",
        "The verification record from the independent audit ruled out this specific reported assignment.",
        "An audit of the entry contradicted the assignment and recorded its status as ruled out.",
        "The independent verification record for this catalogue entry classified the reported assignment as ruled out.",
    ),
    "U": (
        "An audit left the reported assignment unresolved.",
        "The independent audit left the reported assignment unresolved.",
        "The independent verification record left the reported assignment unresolved.",
        "An independent review determined that the reported assignment remained unresolved.",
        "The verification record from the independent audit left this specific reported assignment unresolved.",
        "An audit of the entry left the assignment open and recorded its status as unresolved.",
        "The independent verification record for this catalogue entry classified the reported assignment as unresolved.",
    ),
    "N": (
        "The archive lists the report in its catalogue.",
        "An entry in the catalogue lists this report.",
        "The catalogue index includes an entry for this report.",
        "The central catalogue index files this report under its source.",
        "The central index files this report in the catalogue under its source.",
        "The catalogue index places this entry alongside other reports filed by the same source.",
        "The central catalogue index places this entry alongside other reports filed by the same source.",
        "The catalogue index records the entry as one of several reports filed under this source.",
    ),
}

PROSE_LINKS = ("In the first entry of the catalogue, ", "In the next entry of the catalogue, ",
               "Elsewhere in the same catalogue, ")

REVIEW_LEADS = ("", "Here, ", "For this entry, ", "In the catalogue, ",
                "For this catalogue entry, ", "For this particular entry, ")

def cue_bank():
    return {s: [lead+sentence[0].lower()+sentence[1:] if lead else sentence
                for lead in REVIEW_LEADS for sentence in sentences]
            for s, sentences in CUE_SENTENCES.items()}

def record_text(form, ordinal, fact, sentence):
    if form == "records":
        return f"Report {ordinal+1}: {fact} Review: {sentence}"
    connector = PROSE_LINKS[0 if ordinal == 0 else 1+(ordinal-1)%2]
    return f"{connector}{fact} {sentence}"
