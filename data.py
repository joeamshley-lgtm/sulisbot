import random

# --- 1. SYNONYMS (Word -> Synonym) ---
synonyms = {
    "ephemeral": "fleeting",
    "ubiquitous": "everywhere",
    "profound": "deep",
    "ambiguous": "unclear",
    "pragmatic": "practical",
    "melancholy": "sorrow",
    "inevitable": "unavoidable",
    "paradigm": "model"
}

# --- 2. LITERARY TERMS (Definition -> Term) ---
literary_terms = {
    "Multiple independent voices or perspectives within a single narrative": "polyphony",
    "A narrator whose credibility is compromised or structurally fragmented": "unreliable narrator",
    "A recurring symbol, concept, or theme in a narrative": "motif",
    "A character who contrasts with another to highlight specific traits": "foil",
    "A narrative style reflecting the uninterrupted flow of inner thoughts": "stream of consciousness",
    "Placing two concepts side by side to highlight their contrast": "juxtaposition",
    "An indirect reference to another literary work or historical event": "allusion"
}

# --- 3. PSYCHOANALYTIC VOCABULARY (Definition -> Term) ---
psych_vocab = {
    "Winnicott's concept of the authentic, spontaneous core of the personality": "true self",
    "Winnicott's concept of a defensive facade created to protect the ego": "false self",
    "An item used by a child to provide psychological comfort, like a blanket": "transitional object",
    "A nurturing space that allows for healthy psychological development": "holding environment",
    "Attributing one's own unacceptable feelings or impulses to someone else": "projection",
    "Burying distressing memories or thoughts deep in the unconscious": "repression",
    "The process of breaking a complex topic or personality down into smaller, fragmented parts": "analysis"
}

# --- RANDOMIZER FUNCTIONS ---
def random_synonym():
    # Returns (Word, Answer) -> e.g., ("ephemeral", "fleeting")
    return random.choice(list(synonyms.items()))

def random_literature():
    # Returns (Definition, Answer) -> e.g., ("Multiple independent voices...", "polyphony")
    return random.choice(list(literary_terms.items()))

def random_psych():
    # Returns (Definition, Answer) -> e.g., ("Winnicott's concept of...", "true self")
    return random.choice(list(psych_vocab.items()))
