from random import randint

refusals = ["No.", "Nope.", "Not happening.", "Absolutely not.", "How about no?", "No can has.", "Oof.",
            "NO GOD PLEASE NO.", "WHY?!", "Stop!", "Begone.", "Oof.", "Madness!", "Oi.", "kthxnope",
            "You're really asking for it aren't you?"]


def random_refusal_message():
    return refusals[randint(0, len(refusals) - 1)]
