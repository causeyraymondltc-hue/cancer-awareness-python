"""
CancerGuard AI Assistant - retrieval over a curated knowledge base.
No generative model is used. Answers come only from cancer_content.py,
so the assistant cannot invent medical claims.
"""

from cancer_content import (
    CANCER_LIBRARY,
    MYTHS,
    SYMPTOM_GUIDE,
    NEXT_STEPS,
    EMERGENCY_SIGNS,
    DOCTOR_QUESTIONS,
    DISCLAIMER
)

EMERGENCY_KEYWORDS = [
    "cannot breathe", "can't breathe", "severe bleeding", "heavy bleeding",
    "unconscious", "collapsed", "seizure", "chest pain", "coughing blood",
    "coughing up blood", "severe pain"
]

CRISIS_KEYWORDS = [
    "kill myself", "suicide", "end my life", "want to die", "self harm"
]

GENERAL_ANSWERS = {
    ("prevent", "prevention", "reduce risk", "lower risk"): (
        "Evidence-based ways to lower cancer risk include avoiding tobacco, "
        "limiting alcohol, staying physically active, eating a balanced diet with "
        "vegetables, fruit and whole grains, maintaining a healthy weight, "
        "protecting your skin from ultraviolet radiation, considering HPV and "
        "hepatitis B vaccination where appropriate, and attending recommended "
        "screening."
    ),
    ("hpv",): (
        "HPV is human papillomavirus, a common infection. Persistent infection "
        "with high-risk types can lead to cervical and some other cancers. "
        "Vaccination and cervical screening greatly reduce this risk."
    ),
    ("screening", "screened"): (
        "Screening looks for cancer or pre-cancer in people without symptoms. "
        "Diagnosis happens when tests are done because of symptoms or an abnormal "
        "screening result. Which screening applies to you depends on your age, "
        "sex, risk factors and country."
    ),
    ("chemotherapy", "chemo"): (
        "Chemotherapy uses medicines that target rapidly dividing cells. It may be "
        "given before or after surgery, or on its own. Side effects vary by drug "
        "and person, and your care team can explain what to expect."
    ),
    ("radiotherapy", "radiation"): (
        "Radiotherapy uses targeted radiation to damage cancer cells in a specific "
        "area. It is usually given over several sessions and is planned carefully "
        "to limit effects on healthy tissue."
    ),
    ("biopsy",): (
        "A biopsy removes a small tissue sample so it can be examined under a "
        "microscope. It is the most reliable way to confirm whether cells are "
        "cancerous. Biopsies do not cause cancer to spread."
    ),
    ("smoking", "tobacco", "quit"): (
        "Tobacco is the largest preventable cause of cancer. Quitting reduces risk "
        "at any age. Support such as counselling and approved medicines improves "
        "the chance of quitting successfully."
    ),
    ("alcohol",): (
        "Alcohol is linked to cancers of the mouth, throat, oesophagus, liver, "
        "bowel and breast. Less alcohol means lower risk, and no amount is "
        "considered completely risk free."
    ),
    ("question", "ask my doctor", "ask the doctor"): (
        "Useful questions include: " + " ".join(DOCTOR_QUESTIONS)
    ),
    ("what is cancer", "define cancer"): (
        "Cancer is a group of diseases in which abnormal cells grow uncontrollably "
        "and can spread to other parts of the body. There are many different types "
        "with different causes, treatments and outcomes."
    )
}


def _match_cancer(question):
    lowered = question.lower()
    for name, data in CANCER_LIBRARY.items():
        key = name.lower().replace(" cancer", "")
        if key in lowered:
            return name, data
    return None, None


def _match_myth(question):
    lowered = question.lower()
    for myth in MYTHS:
        words = [
            word for word in myth["claim"].lower().replace(".", "").split()
            if len(word) > 4
        ]
        hits = sum(1 for word in words if word in lowered)
        if hits >= 2:
            return myth
    return None


def _match_symptom(question):
    lowered = question.lower()
    keywords = {
        "lump": "A new lump anywhere on the body",
        "weight": "Unexplained weight loss",
        "cough": "A cough lasting more than three weeks",
        "stool": "Change in bowel habit or blood in stool",
        "bowel": "Change in bowel habit or blood in stool",
        "bleeding": "Unusual vaginal bleeding",
        "mole": "A mole or skin change",
        "ulcer": "A mouth ulcer that does not heal",
        "tired": "Persistent unexplained tiredness",
        "swallow": "Difficulty swallowing",
        "urine": "Urinary changes or blood in urine"
    }
    for word, symptom in keywords.items():
        if word in lowered:
            return symptom, SYMPTOM_GUIDE[symptom]
    return None, None


def answer_question(question):
    """Return a dictionary with the assistant reply."""
    if not question or not question.strip():
        return {
            "type": "empty",
            "text": "Please type a question about cancer prevention or awareness."
        }

    lowered = question.lower()

    for word in CRISIS_KEYWORDS:
        if word in lowered:
            return {
                "type": "crisis",
                "text": (
                    "It sounds like you may be going through something very "
                    "difficult. Please contact a local emergency number, a crisis "
                    "helpline, or a trusted person right now. You deserve support "
                    "from a real person."
                )
            }

    for word in EMERGENCY_KEYWORDS:
        if word in lowered:
            return {
                "type": "emergency",
                "text": (
                    "The symptom you described may need urgent medical attention. "
                    "Please contact emergency services or go to the nearest "
                    "emergency department now. Do not wait for online information."
                ),
                "list": EMERGENCY_SIGNS
            }

    myth = _match_myth(question)
    if myth:
        return {
            "type": "myth",
            "text": myth["explanation"],
            "claim": myth["claim"],
            "verdict": myth["verdict"]
        }

    symptom, guide = _match_symptom(question)
    if symptom:
        return {
            "type": "symptom",
            "topic": symptom,
            "text": guide["explanation"],
            "action": guide["action"],
            "list": NEXT_STEPS
        }

    name, data = _match_cancer(question)
    if name:
        if "sign" in lowered or "symptom" in lowered or "warning" in lowered:
            return {
                "type": "cancer_signs",
                "topic": name,
                "text": f"Possible warning signs associated with {name.lower()}:",
                "list": data["warning_signs"]
            }
        if "prevent" in lowered or "reduce" in lowered:
            return {
                "type": "cancer_prevention",
                "topic": name,
                "text": f"Ways that may reduce risk related to {name.lower()}:",
                "list": data["prevention"]
            }
        if "screen" in lowered or "test" in lowered:
            return {
                "type": "cancer_screening",
                "topic": name,
                "text": data["screening"]
            }
        if "risk" in lowered or "cause" in lowered:
            return {
                "type": "cancer_risk",
                "topic": name,
                "text": f"Risk factors associated with {name.lower()}:",
                "list": data["risk_factors"]
            }
        return {
            "type": "cancer_overview",
            "topic": name,
            "text": data["what_it_is"],
            "list": data["warning_signs"]
        }

    for keywords, response in GENERAL_ANSWERS.items():
        for keyword in keywords:
            if keyword in lowered:
                return {
                    "type": "general",
                    "text": response
                }

    return {
        "type": "unknown",
        "text": (
            "I do not have curated information for that question yet. Try asking "
            "about a specific cancer type, prevention, screening, warning signs, "
            "or a common cancer myth. For personal medical concerns, please speak "
            "with a qualified healthcare professional."
        )
    }


def get_disclaimer():
    return DISCLAIMER