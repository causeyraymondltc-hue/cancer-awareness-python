"""
CancerGuard AI - Educational content module.
General health education based on public health guidance
(WHO, IARC, CDC, NCI). Not medical advice. Does not diagnose.
"""

DISCLAIMER = (
    "This information is general health education only. It does not diagnose "
    "any condition and does not replace assessment by a qualified healthcare "
    "professional. If you have symptoms or concerns, seek medical care."
)

SOURCES = "General public health guidance: WHO, IARC, CDC, NCI."


CANCER_LIBRARY = {
    "Breast cancer": {
        "what_it_is": (
            "Breast cancer begins when cells in the breast grow abnormally. "
            "It can affect women and, less commonly, men. Many breast changes "
            "are not cancer, but new changes should always be assessed."
        ),
        "risk_factors": [
            "Increasing age",
            "Family history of breast or ovarian cancer",
            "Alcohol consumption",
            "Excess body weight, especially after menopause",
            "Physical inactivity",
            "Certain inherited gene changes such as BRCA1 and BRCA2"
        ],
        "prevention": [
            "Limit or avoid alcohol",
            "Maintain regular physical activity",
            "Work toward a healthy body weight",
            "Discuss family history with a healthcare professional",
            "Attend screening appropriate for your age and risk"
        ],
        "warning_signs": [
            "A new lump or thickening in the breast or underarm",
            "Change in breast size or shape",
            "Skin dimpling or puckering",
            "Nipple change, inversion or unusual discharge",
            "Persistent breast pain in one area"
        ],
        "screening": (
            "Mammography screening is commonly recommended for women in "
            "specific age ranges. Exact ages and intervals vary by country "
            "and personal risk. Ask a healthcare professional what applies to you."
        ),
        "seek_care": (
            "Arrange a medical evaluation for any new lump, skin change, "
            "nipple change or persistent breast symptom."
        )
    },

    "Cervical cancer": {
        "what_it_is": (
            "Cervical cancer develops in the cervix and is strongly linked to "
            "persistent infection with high-risk human papillomavirus. "
            "It is one of the most preventable cancers."
        ),
        "risk_factors": [
            "Persistent high-risk HPV infection",
            "Not being vaccinated against HPV",
            "Never or rarely attending cervical screening",
            "Smoking",
            "Weakened immune system, including untreated HIV"
        ],
        "prevention": [
            "HPV vaccination where medically appropriate",
            "Regular cervical screening as recommended locally",
            "Avoid tobacco",
            "Seek treatment for precancerous changes when advised"
        ],
        "warning_signs": [
            "Bleeding between periods or after sex",
            "Bleeding after menopause",
            "Unusual or persistent vaginal discharge",
            "Pelvic pain"
        ],
        "screening": (
            "Screening may include HPV testing, cytology, or visual inspection "
            "depending on the country. Screening prevents cancer by detecting "
            "and treating changes before cancer develops."
        ),
        "seek_care": (
            "Report unexpected vaginal bleeding, especially after sex or after "
            "menopause, to a healthcare professional."
        )
    },

    "Prostate cancer": {
        "what_it_is": (
            "Prostate cancer develops in the prostate gland in men. Many "
            "prostate cancers grow slowly, while some are more aggressive."
        ),
        "risk_factors": [
            "Increasing age",
            "Family history of prostate cancer",
            "African ancestry, which is associated with higher risk",
            "Excess body weight"
        ],
        "prevention": [
            "Maintain a healthy body weight",
            "Stay physically active",
            "Eat a balanced diet",
            "Discuss family history and testing options with a doctor"
        ],
        "warning_signs": [
            "Difficulty starting or stopping urination",
            "Weak urinary stream",
            "Frequent urination, especially at night",
            "Blood in urine or semen",
            "Persistent pelvic, hip or back pain"
        ],
        "screening": (
            "PSA blood testing is available in many settings, but benefits and "
            "harms differ between individuals. This is a shared decision to make "
            "with a healthcare professional."
        ),
        "seek_care": (
            "Discuss ongoing urinary changes or blood in urine with a doctor."
        )
    },

    "Colorectal cancer": {
        "what_it_is": (
            "Colorectal cancer affects the colon or rectum. It often develops "
            "from growths called polyps, which can be removed during screening."
        ),
        "risk_factors": [
            "Increasing age",
            "Family history of colorectal cancer or polyps",
            "Diets high in processed and red meat",
            "Low fibre intake",
            "Physical inactivity and excess body weight",
            "Tobacco and alcohol use",
            "Inflammatory bowel disease"
        ],
        "prevention": [
            "Increase fibre from vegetables, fruit and whole grains",
            "Limit processed meat",
            "Stay physically active",
            "Avoid tobacco and limit alcohol",
            "Attend screening when recommended"
        ],
        "warning_signs": [
            "Blood in stool or rectal bleeding",
            "Persistent change in bowel habit",
            "Ongoing abdominal pain or bloating",
            "Unexplained weight loss",
            "Unexplained tiredness or anaemia"
        ],
        "screening": (
            "Stool tests and colonoscopy are widely used. Screening can prevent "
            "cancer by removing polyps before they become cancerous."
        ),
        "seek_care": (
            "Report rectal bleeding or a bowel habit change lasting more than a "
            "few weeks to a healthcare professional."
        )
    },

    "Lung cancer": {
        "what_it_is": (
            "Lung cancer develops in the lungs and is strongly associated with "
            "tobacco smoke, although non-smokers can also develop it."
        ),
        "risk_factors": [
            "Smoking tobacco, the leading cause",
            "Secondhand smoke",
            "Air pollution",
            "Occupational exposures such as asbestos",
            "Radon exposure",
            "Family history"
        ],
        "prevention": [
            "Do not start smoking, and seek support to quit",
            "Avoid secondhand smoke",
            "Reduce exposure to indoor smoke and pollution",
            "Use protective measures for occupational exposures"
        ],
        "warning_signs": [
            "A cough that does not go away or worsens",
            "Coughing up blood",
            "Breathlessness",
            "Chest pain",
            "Repeated chest infections",
            "Unexplained weight loss"
        ],
        "screening": (
            "Low-dose CT screening is offered in some countries for people with "
            "significant smoking history. Availability varies."
        ),
        "seek_care": (
            "Seek prompt medical care for coughing up blood, or a cough lasting "
            "more than three weeks."
        )
    },

    "Liver cancer": {
        "what_it_is": (
            "Liver cancer often develops in livers already affected by long-term "
            "damage, especially from chronic hepatitis B or C infection."
        ),
        "risk_factors": [
            "Chronic hepatitis B or hepatitis C infection",
            "Heavy alcohol use",
            "Cirrhosis from any cause",
            "Fatty liver disease",
            "Aflatoxin exposure from poorly stored grains and nuts"
        ],
        "prevention": [
            "Hepatitis B vaccination where appropriate",
            "Testing and treatment for hepatitis B and C",
            "Limit alcohol",
            "Store food properly to reduce aflatoxin exposure",
            "Maintain a healthy weight"
        ],
        "warning_signs": [
            "Upper abdominal pain or swelling",
            "Yellowing of eyes or skin",
            "Unexplained weight loss",
            "Loss of appetite",
            "Persistent tiredness"
        ],
        "screening": (
            "People with chronic hepatitis or cirrhosis may be offered regular "
            "surveillance. Discuss this with a healthcare professional."
        ),
        "seek_care": (
            "Yellowing of the eyes or skin should be assessed promptly."
        )
    },

    "Skin cancer": {
        "what_it_is": (
            "Skin cancer develops in skin cells, most often due to ultraviolet "
            "radiation damage. Melanoma is the most serious common type."
        ),
        "risk_factors": [
            "High ultraviolet exposure and sunburn history",
            "Use of tanning devices",
            "Fair skin that burns easily",
            "Many moles or unusual moles",
            "Family or personal history of skin cancer",
            "Weakened immune system"
        ],
        "prevention": [
            "Seek shade during peak ultraviolet hours",
            "Wear protective clothing and a hat",
            "Use broad-spectrum sunscreen correctly",
            "Avoid tanning devices",
            "Check your skin regularly for changes"
        ],
        "warning_signs": [
            "A mole that changes in size, shape or colour",
            "A mole with an irregular border or uneven colour",
            "A sore that does not heal",
            "A new growing lump or scaly patch",
            "Itching or bleeding from a skin lesion"
        ],
        "screening": (
            "Routine population screening is not standard everywhere, but skin "
            "checks may be advised for higher-risk individuals."
        ),
        "seek_care": (
            "Show any changing or non-healing skin lesion to a doctor."
        )
    },

    "Oral cancer": {
        "what_it_is": (
            "Oral cancer affects the lips, tongue, gums, and lining of the mouth "
            "and throat."
        ),
        "risk_factors": [
            "Tobacco smoking and smokeless tobacco",
            "Betel quid and areca nut chewing",
            "Alcohol use, especially combined with tobacco",
            "HPV infection",
            "Prolonged sun exposure affecting the lips"
        ],
        "prevention": [
            "Avoid all tobacco products and betel quid",
            "Limit alcohol",
            "HPV vaccination where appropriate",
            "Attend regular dental check-ups",
            "Protect lips from sun exposure"
        ],
        "warning_signs": [
            "A mouth ulcer that does not heal within three weeks",
            "A white or red patch in the mouth",
            "Persistent hoarseness",
            "Difficulty or pain when swallowing",
            "A lump in the neck"
        ],
        "screening": (
            "Dental and clinical mouth examinations can help detect early changes."
        ),
        "seek_care": (
            "A mouth ulcer lasting longer than three weeks should be examined."
        )
    },

    "Childhood cancers": {
        "what_it_is": (
            "Childhood cancers include leukaemia, brain tumours, lymphomas and "
            "others. Many are treatable, and early evaluation matters."
        ),
        "risk_factors": [
            "Most childhood cancers have no identifiable preventable cause",
            "A small number relate to inherited genetic conditions",
            "Some relate to previous radiation exposure or specific infections"
        ],
        "prevention": [
            "Childhood cancers are usually not preventable",
            "Focus on early recognition and prompt medical assessment",
            "Keep routine vaccinations up to date"
        ],
        "warning_signs": [
            "Unexplained persistent fever or paleness",
            "Easy bruising or bleeding",
            "A lump or swelling anywhere on the body",
            "Persistent bone or joint pain",
            "Unexplained weight loss",
            "Persistent morning headache with vomiting",
            "White reflection in the eye pupil"
        ],
        "screening": (
            "There is no routine population screening for childhood cancer. "
            "Early evaluation of persistent symptoms is the main approach."
        ),
        "seek_care": (
            "Take a child with persistent unexplained symptoms to a healthcare "
            "professional without delay."
        )
    }
}


EMERGENCY_SIGNS = [
    "Severe difficulty breathing",
    "Heavy or uncontrolled bleeding",
    "Severe chest pain",
    "Coughing up large amounts of blood",
    "Sudden weakness, confusion or loss of consciousness",
    "Severe uncontrolled pain",
    "Seizure"
]

SYMPTOM_GUIDE = {
    "A new lump anywhere on the body": {
        "explanation": (
            "Most lumps are not cancer. Cysts, infections and benign growths are "
            "common. However, a new lump that persists, grows, or feels hard and "
            "fixed should always be assessed."
        ),
        "action": "Arrange a medical evaluation, especially if it persists beyond two weeks."
    },
    "Unexplained weight loss": {
        "explanation": (
            "Losing weight without trying can have many causes, including thyroid "
            "problems, infection, diabetes and digestive conditions."
        ),
        "action": "See a healthcare professional if you lose weight without trying."
    },
    "A cough lasting more than three weeks": {
        "explanation": (
            "Persistent cough is often due to infection, asthma, reflux or air "
            "quality. It still needs assessment when it does not settle."
        ),
        "action": "Seek medical assessment, and urgent care if you cough up blood."
    },
    "Change in bowel habit or blood in stool": {
        "explanation": (
            "Haemorrhoids and infections are common causes, but bleeding and "
            "persistent bowel changes should never be ignored."
        ),
        "action": "See a healthcare professional if changes last more than a few weeks."
    },
    "Unusual vaginal bleeding": {
        "explanation": (
            "Bleeding between periods, after sex or after menopause has several "
            "possible causes and requires assessment."
        ),
        "action": "Arrange a gynaecological evaluation."
    },
    "A mole or skin change": {
        "explanation": (
            "Look for change in size, shape, colour, irregular borders, itching, "
            "bleeding, or a sore that does not heal."
        ),
        "action": "Show the lesion to a doctor or dermatologist."
    },
    "A mouth ulcer that does not heal": {
        "explanation": (
            "Most mouth ulcers heal within two weeks. Those lasting longer than "
            "three weeks need examination."
        ),
        "action": "See a dentist or doctor."
    },
    "Persistent unexplained tiredness": {
        "explanation": (
            "Fatigue is very common and usually not cancer, but persistent "
            "unexplained fatigue with other symptoms should be checked."
        ),
        "action": "Discuss with a healthcare professional, especially with other symptoms."
    },
    "Difficulty swallowing": {
        "explanation": (
            "Reflux and infections commonly cause this, but persistent difficulty "
            "swallowing needs evaluation."
        ),
        "action": "Seek medical assessment if it persists beyond three weeks."
    },
    "Urinary changes or blood in urine": {
        "explanation": (
            "Infections and prostate enlargement are common causes, but blood in "
            "urine always needs assessment."
        ),
        "action": "Book a medical appointment."
    }
}

NEXT_STEPS = [
    "Do not panic. Most symptoms are caused by conditions other than cancer.",
    "Do not attempt to diagnose yourself online.",
    "Write down when the change started and whether it is getting worse.",
    "Book an appointment with a qualified healthcare professional.",
    "Ask whether any tests or referral are appropriate.",
    "Seek urgent or emergency care for severe symptoms."
]


MYTHS = [
    {
        "claim": "Cancer is contagious.",
        "verdict": "False",
        "explanation": (
            "Cancer cannot be caught from another person. Some infections that "
            "increase cancer risk, such as HPV, hepatitis B and hepatitis C, can "
            "be transmitted, but the cancer itself is not contagious."
        )
    },
    {
        "claim": "Sugar directly causes cancer.",
        "verdict": "Misleading",
        "explanation": (
            "Sugar does not directly cause cancer. However, excess calorie intake "
            "can contribute to excess body weight, which is associated with "
            "increased risk of several cancers."
        )
    },
    {
        "claim": "Cancer is always a death sentence.",
        "verdict": "False",
        "explanation": (
            "Many cancers are treatable, and survival has improved for many types, "
            "particularly when detected early and treated appropriately."
        )
    },
    {
        "claim": "Herbal medicine can cure all cancers.",
        "verdict": "False and potentially dangerous",
        "explanation": (
            "No herbal product is proven to cure cancer. Delaying evidence-based "
            "treatment can allow the disease to progress. Always discuss any "
            "supplement with your treating team, as some interact with treatment."
        )
    },
    {
        "claim": "If there is no pain, there is no cancer.",
        "verdict": "False",
        "explanation": (
            "Many early cancers cause no pain at all. This is exactly why "
            "screening and early evaluation of changes matter."
        )
    },
    {
        "claim": "Only older people get cancer.",
        "verdict": "False",
        "explanation": (
            "Risk increases with age, but cancer can occur at any age, including "
            "in children and young adults."
        )
    },
    {
        "claim": "A biopsy causes cancer to spread.",
        "verdict": "False",
        "explanation": (
            "Biopsy is a standard, safe diagnostic procedure. Avoiding it delays "
            "diagnosis and appropriate treatment."
        )
    },
    {
        "claim": "Cancer is caused by witchcraft or a curse.",
        "verdict": "False",
        "explanation": (
            "Cancer is a biological disease caused by changes in cells. Believing "
            "otherwise can delay life-saving medical care."
        )
    },
    {
        "claim": "Mobile phones cause brain cancer.",
        "verdict": "Not established",
        "explanation": (
            "Current evidence has not established that mobile phone use causes "
            "brain cancer. Research continues."
        )
    },
    {
        "claim": "If nobody in my family had cancer, I cannot get it.",
        "verdict": "False",
        "explanation": (
            "Most cancers occur in people with no family history. Lifestyle, "
            "infections, environment and age all contribute."
        )
    }
]


def screening_guidance(age, sex, smoking_history, family_history, hepatitis):
    """Return a list of educational screening awareness items."""
    items = []

    if sex in ("Female", "Prefer not to say"):
        if age >= 25:
            items.append({
                "area": "Cervical cancer",
                "status": "Learn about cervical screening",
                "note": "Screening usually begins in the twenties or thirties depending on the country."
            })
        if age >= 40:
            items.append({
                "area": "Breast cancer",
                "status": "Discuss appropriate breast screening",
                "note": "Programme ages vary. Earlier discussion is common with family history."
            })
        else:
            items.append({
                "area": "Breast awareness",
                "status": "Know what is normal for you",
                "note": "Report any new lump or breast change regardless of age."
            })

    if sex in ("Male", "Prefer not to say"):
        if age >= 45:
            items.append({
                "area": "Prostate cancer",
                "status": "Discuss testing options with a doctor",
                "note": "PSA testing is a shared decision that weighs benefits and harms."
            })

    if age >= 45:
        items.append({
            "area": "Colorectal cancer",
            "status": "Learn about bowel screening",
            "note": "Many programmes begin between ages 45 and 50."
        })

    if smoking_history in ("Current smoker", "Former smoker"):
        items.append({
            "area": "Lung cancer",
            "status": "Ask whether lung screening is available to you",
            "note": "Low-dose CT screening exists in some countries for higher-risk adults."
        })

    if family_history == "Yes":
        items.append({
            "area": "Family history review",
            "status": "Request a family history assessment",
            "note": "You may qualify for earlier or additional screening."
        })

    if hepatitis == "Yes":
        items.append({
            "area": "Liver surveillance",
            "status": "Discuss liver monitoring",
            "note": "Chronic hepatitis may require regular liver surveillance."
        })

    items.append({
        "area": "Skin awareness",
        "status": "Check your skin regularly",
        "note": "Report changing moles or non-healing sores."
    })

    return items


CARE_JOURNEY = [
    ("Awareness", "Learn about cancer, risk factors and prevention."),
    ("Prevention", "Reduce modifiable risks such as tobacco, alcohol and inactivity."),
    ("Screening", "Attend age-appropriate and risk-appropriate screening."),
    ("Noticing a change", "Recognise a symptom or receive an abnormal screening result."),
    ("Clinical evaluation", "A healthcare professional examines you and takes a history."),
    ("Diagnostic testing", "Imaging, laboratory tests or biopsy may be arranged."),
    ("Diagnosis", "A specialist explains the findings and what they mean."),
    ("Treatment planning", "A care team discusses options and your preferences."),
    ("Treatment", "This may include surgery, radiotherapy, medicines or a combination."),
    ("Follow-up", "Monitoring for recovery, side effects and recurrence."),
    ("Survivorship and support", "Physical, emotional, social and financial support continues.")
]

DOCTOR_QUESTIONS = [
    "What could be causing my symptom?",
    "Which tests do I need and why?",
    "How soon will I get the results?",
    "Do I need a referral to a specialist?",
    "What should I watch for while I wait?",
    "What are my treatment options and their side effects?",
    "What support services are available to me?"
]


SUPPORT_TOPICS = {
    "I am worried about cancer": (
        "Worry is a normal response. Write down what you have noticed and when it "
        "started, then book a medical appointment. Getting checked usually reduces "
        "anxiety, and most symptoms turn out to be caused by something else."
    ),
    "Someone I love has cancer": (
        "Practical help is often more valuable than advice. Offer transport, meals, "
        "help with appointments, or simply listening. Ask what they want rather than "
        "assuming, and look after your own wellbeing too."
    ),
    "I received a cancer diagnosis": (
        "Ask your care team to explain the diagnosis in plain language, bring someone "
        "with you to appointments, and write questions down beforehand. You can ask "
        "for a second opinion and for information in your own language."
    ),
    "How do I support someone emotionally": (
        "Listen without trying to fix everything. Avoid saying that you know exactly "
        "how they feel. Keep contact steady over time, not just at the beginning."
    ),
    "How do I talk to my family": (
        "Choose a calm time, share what you know, and be honest about uncertainty. "
        "Children generally cope better with simple, truthful explanations suited to "
        "their age."
    ),
    "Managing fear and stress": (
        "Regular sleep, activity, and social contact help. Limit late-night searching "
        "online. If fear affects daily life, ask a healthcare professional about "
        "counselling or mental health support."
    )
}


CARE_FACILITIES = {
    "Ekiti": [
        {
            "name": "Ekiti State University Teaching Hospital",
            "type": "Teaching hospital",
            "city": "Ado-Ekiti",
            "services": "General care, diagnostics, specialist referral"
        },
        {
            "name": "Federal Teaching Hospital Ido-Ekiti",
            "type": "Teaching hospital",
            "city": "Ido-Ekiti",
            "services": "General care, diagnostics, oncology referral"
        }
    ],
    "Lagos": [
        {
            "name": "Lagos University Teaching Hospital",
            "type": "Teaching hospital",
            "city": "Idi-Araba, Lagos",
            "services": "Oncology, radiotherapy, diagnostics"
        },
        {
            "name": "Lagos State University Teaching Hospital",
            "type": "Teaching hospital",
            "city": "Ikeja, Lagos",
            "services": "Oncology services and diagnostics"
        }
    ],
    "Oyo": [
        {
            "name": "University College Hospital",
            "type": "Teaching hospital",
            "city": "Ibadan",
            "services": "Oncology, radiotherapy, diagnostics"
        }
    ],
    "FCT Abuja": [
        {
            "name": "National Hospital Abuja",
            "type": "Tertiary hospital",
            "city": "Abuja",
            "services": "Oncology and diagnostic services"
        }
    ]
}

CARE_PATHWAY = [
    "Primary health centre or general practitioner for first assessment",
    "General or district hospital for initial tests",
    "Teaching or tertiary hospital for specialist evaluation",
    "Diagnostic laboratory or imaging centre for tests",
    "Oncology centre for treatment planning"
]