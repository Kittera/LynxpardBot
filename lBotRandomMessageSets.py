from random import randint

refusals = ["No.", "Nope.", "Not happening.", "Absolutely not.", "How about no?", "No can has.", "Oof.",
            "NO GOD PLEASE NO.", "WHY?!", "Stop! You've violated the law!", "Begone.", "Oof.", "Madness!", "Oi.",
            "kthxnope", "You're really asking for it aren't you?", '<:nomegusta:799363442213519391>']


def random_refusal_message():
    return refusals[randint(0, len(refusals) - 1)]
