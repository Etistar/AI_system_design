"""Small safety router used by the prototype before the two CrewAI agents run."""

EMERGENCY_TERMS = (
    "chest pain",
    "heart attack",
    "can't breathe",
    "cannot breathe",
    "trouble breathing",
    "shortness of breath",
    "stroke",
    "face droop",
    "slurred speech",
    "suicidal",
    "kill myself",
    "want to die",
    "overdose",
    "not breathing",
    "severe bleeding",
    "anaphylaxis",
    "lips are swelling",
)

EMERGENCY_MESSAGE = """This question describes a possible emergency. The research crew will not answer it.

Contact local emergency services now. If this is about self-harm, contact a local crisis line and stay with a trusted person if you can.

A research summary is not the right tool for chest pain, stroke signs, trouble breathing, overdose, severe allergy, or intent to self-harm."""


def is_emergency(question: str) -> bool:
    text = question.casefold()
    return any(term in text for term in EMERGENCY_TERMS)
