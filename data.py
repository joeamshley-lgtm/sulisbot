import random

synonyms = {
    "happy": "joyful",
    "sad": "unhappy",
}

literary_terms = {
    "stream of consciousness": "narrative style reflecting thoughts"
}

psych_vocab = {
    "narcissism": "excessive self-focus"
}


def random_synonym():
    return random.choice(list(synonyms.items()))

def random_literature():
    return random.choice(list(literary_terms.items()))

def random_psych():
    return random.choice(list(psych_vocab.items()))