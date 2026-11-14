import re


# ============================================================
# CLAUSE DEFINITIONS
# ============================================================

CLAUSE_PATTERNS = {
    "Payment": [
        r"\bpayment\b",
        r"\binvoice\b",
        r"\bfees?\b",
        r"\bpayable\b",
        r"\bnet\s*30\b",
        r"\b\d+\s*days?\s*(?:from|after)\s+(?:the\s+)?invoice\b",
        r"\bpayment\s+terms?\b",
    ],

    "Termination": [
        r"\btermination\b",
        r"\bterminate\b",
        r"\bterminated\b",
        r"\bnotice\s+period\b",
        r"\bnotice\s+of\s+termination\b",
    ],

    "Confidentiality": [
        r"\bconfidential(?:ity)?\b",
        r"\bnon[-\s]?disclosure\b",
        r"\bnondisclosure\b",
        r"\bconfidential\s+information\b",
    ],

    "Liability": [
        r"\bliability\b",
        r"\bliable\b",
        r"\bdamages\b",
        r"\bindemnification\b",
        r"\bindemnity\b",
    ],

    "Force Majeure": [
        r"\bforce\s+majeure\b",
        r"\bacts?\s+of\s+god\b",
        r"\bnatural\s+disaster\b",
        r"\bearthquake\b",
        r"\bflood\b",
        r"\bpandemic\b",
        r"\bepidemic\b",
        r"\bwar\b",
    ],

    "Renewal": [
        r"\brenewal\b",
        r"\brenew\b",
        r"\brenewed\b",
        r"\bautomatically\s+renew\b",
        r"\bautomatic\s+renewal\b",
    ],

    "Governing Law": [
        r"\bgoverning\s+law\b",
        r"\blaws\s+of\b",
        r"\bgoverned\s+by\s+the\s+laws?\b",
        r"\bjurisdiction\b",
    ],

    "Arbitration": [
        r"\barbitration\b",
        r"\barbitrator\b",
        r"\bdispute\s+resolution\b",
        r"\bcommercial\s+arbitration\b",
    ],
}


# ============================================================
# HELPER
# ============================================================

def contains_pattern(text: str, pattern: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE) is not None


# ============================================================
# CLAUSE DETECTION
# ============================================================

def detect_clauses(text: str):

    text_lower = text.lower()

    detected = []

    for clause_name, patterns in CLAUSE_PATTERNS.items():

        matched_keywords = []

        for pattern in patterns:

            if contains_pattern(text_lower, pattern):

                # Convert regex patterns into readable keywords
                readable = (
                    pattern
                    .replace(r"\b", "")
                    .replace(r"\s+", " ")
                    .replace("?", "")
                )

                if readable not in matched_keywords:
                    matched_keywords.append(readable)

        if matched_keywords:

            detected.append({
                "clause": clause_name,
                "keywords": matched_keywords,
                "status": "Detected",
            })

    return detected


# ============================================================
# MISSING CLAUSES
# ============================================================

def detect_missing_clauses(text: str, detected_clauses):

    detected_names = {
        item["clause"]
        for item in detected_clauses
    }

    missing = []

    for clause_name in CLAUSE_PATTERNS:

        if clause_name not in detected_names:

            # Payment is more important than optional clauses
            if clause_name == "Payment":
                severity = "High"

            elif clause_name in [
                "Termination",
                "Liability",
                "Governing Law",
            ]:
                severity = "Medium"

            else:
                severity = "Low"

            missing.append({
                "clause": clause_name,
                "status": "Missing",
                "severity": severity,
            })

    return missing


# ============================================================
# RISK DETECTION
# ============================================================

def detect_risks(text: str, detected_clauses):

    text_lower = text.lower()

    risks = []

    clause_names = {
        item["clause"]
        for item in detected_clauses
    }


    # --------------------------------------------------------
    # Unlimited Liability
    # --------------------------------------------------------

    unlimited_patterns = [
        r"\bunlimited\s+liability\b",
        r"\bunlimited\s+liability\s+for\b",
        r"\bshall\s+be\s+liable\s+for\s+all\b",
        r"\bwithout\s+limitation\b",
    ]

    if any(
        contains_pattern(text_lower, pattern)
        for pattern in unlimited_patterns
    ):

        risks.append({
            "risk": "Unlimited Liability",
            "severity": "High",
            "explanation": (
                "The agreement may expose a party to "
                "unlimited financial liability."
            ),
        })


    # --------------------------------------------------------
    # Data Privacy
    # --------------------------------------------------------

    privacy_patterns = [
        r"\bdata\s+privacy\b",
        r"\bdata\s+protection\b",
        r"\bpersonal\s+data\b",
        r"\bprivacy\b",
        r"\bgdpr\b",
    ]

    if any(
        contains_pattern(text_lower, pattern)
        for pattern in privacy_patterns
    ):

        risks.append({
            "risk": "Data Privacy",
            "severity": "Medium",
            "explanation": (
                "The agreement contains data/privacy-related "
                "obligations that should be reviewed."
            ),
        })


    # --------------------------------------------------------
    # Short Termination Notice
    # --------------------------------------------------------

    termination_notice = re.search(
        r"\b([0-2]?[0-9])[- ]day[s]?\b.{0,100}\btermination\b",
        text_lower,
        re.IGNORECASE,
    )

    if termination_notice:

        days = int(termination_notice.group(1))

        if days <= 30:

            risks.append({
                "risk": "Short Termination Notice",
                "severity": "Medium",
                "explanation": (
                    f"The contract appears to provide only "
                    f"{days} days of termination notice."
                ),
            })


    # --------------------------------------------------------
    # Missing Force Majeure
    # --------------------------------------------------------

    if "Force Majeure" not in clause_names:

        risks.append({
            "risk": "Missing Force Majeure Clause",
            "severity": "Low",
            "explanation": (
                "No force majeure provision was detected. "
                "Consider reviewing protection against extraordinary events."
            ),
        })


    # --------------------------------------------------------
    # Missing Payment
    # --------------------------------------------------------

    if "Payment" not in clause_names:

        risks.append({
            "risk": "Missing Payment Clause",
            "severity": "Medium",
            "explanation": (
                "No clear payment, invoice, fee or payment-term "
                "provision was detected."
            ),
        })


    # --------------------------------------------------------
    # Missing Governing Law
    # --------------------------------------------------------

    if "Governing Law" not in clause_names:

        risks.append({
            "risk": "Missing Governing Law",
            "severity": "Low",
            "explanation": (
                "The agreement does not clearly specify "
                "the governing law or jurisdiction."
            ),
        })


    return risks


# ============================================================
# OBLIGATION EXTRACTION
# ============================================================

def extract_obligations(text: str):

    obligations = []

    clean_text = re.sub(
        r"\s+",
        " ",
        text.replace("\n", " "),
    ).strip()

    sentences = re.split(
        r"(?<=[.!?])\s+",
        clean_text,
    )

    obligation_patterns = [
        r"\bshall\b",
        r"\bmust\b",
        r"\brequired\s+to\b",
        r"\bobligation\b",
        r"\bnotify\b",
        r"\breturn\b",
        r"\bdestroy\b",
        r"\bcomply\b",
        r"\bpay\b",
        r"\bprovide\b",
        r"\bdeliver\b",
        r"\bmaintain\b",
        r"\bprotect\b",
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 30:
            continue

        if any(
            re.search(
                pattern,
                sentence,
                re.IGNORECASE,
            )
            for pattern in obligation_patterns
        ):

            obligations.append({
                "obligation": sentence
            })


    # Remove duplicates
    unique = []
    seen = set()

    for item in obligations:

        value = item["obligation"].strip()
        normalized = value.lower()

        if normalized not in seen:

            seen.add(normalized)

            unique.append({
                "obligation": value
            })

    return unique[:20]


# ============================================================
# COMPLIANCE ANALYSIS
# ============================================================

def analyze_compliance(text: str):

    text_lower = text.lower()

    compliance = []

    checks = {

        "Data Privacy": [
            r"\bdata\s+privacy\b",
            r"\bdata\s+protection\b",
            r"\bpersonal\s+data\b",
            r"\bprivacy\b",
            r"\bgdpr\b",
        ],

        "Information Security": [
            r"\binformation\s+security\b",
            r"\bsecurity\s+measures\b",
            r"\bsecurity\s+requirements\b",
            r"\bcybersecurity\b",
            r"\bsecurity\b",
        ],

        "Anti-Bribery": [
            r"\banti[-\s]?bribery\b",
            r"\bbribery\b",
            r"\banti[-\s]?corruption\b",
            r"\bcorruption\b",
        ],

        "Export Control": [
            r"\bexport\s+control\b",
            r"\bexport\s+controls\b",
            r"\bexport\s+regulations?\b",
        ],

        "Sanctions": [
            r"\bsanctions\b",
            r"\beconomic\s+sanctions\b",
            r"\btrade\s+sanctions\b",
        ],

        "Corporate Governance": [
            r"\bcorporate\s+governance\b",
            r"\bcorporate\s+compliance\b",
            r"\bgovernance\b",
            r"\bcompliance\s+requirements?\b",
            r"\bapplicable\s+laws?\s+and\s+regulations?\b",
        ],
    }


    for name, patterns in checks.items():

        found = any(
            contains_pattern(text_lower, pattern)
            for pattern in patterns
        )

        compliance.append({
            "framework": name,
            "status": (
                "Detected"
                if found
                else "Not Detected"
            ),
        })

    return compliance


# ============================================================
# RISK SCORE
# ============================================================

def calculate_risk_score(
    risks,
    missing_clauses,
):

    score = 0

    # Actual risks
    for risk in risks:

        severity = risk.get(
            "severity",
            "Low",
        )

        if severity == "High":
            score += 30

        elif severity == "Medium":
            score += 15

        else:
            score += 7


    # Missing clauses
    for clause in missing_clauses:

        severity = clause.get(
            "severity",
            "Low",
        )

        if severity == "High":
            score += 12

        elif severity == "Medium":
            score += 7

        else:
            score += 3


    # Minimum score
    score = max(score, 5)

    # Maximum score
    score = min(score, 100)


    if score >= 70:
        level = "High"

    elif score >= 40:
        level = "Medium"

    else:
        level = "Low"


    return score, level


# ============================================================
# MAIN CONTRACT ANALYZER
# ============================================================

def analyze_contract(text: str):

    clauses = detect_clauses(text)

    missing_clauses = detect_missing_clauses(
        text,
        clauses,
    )

    risks = detect_risks(
        text,
        clauses,
    )

    obligations = extract_obligations(text)

    compliance = analyze_compliance(text)

    risk_score, risk_level = calculate_risk_score(
        risks,
        missing_clauses,
    )

    return {

        "risk_score": risk_score,

        "risk_level": risk_level,

        "clauses": clauses,

        "missing_clauses": missing_clauses,

        "risks": risks,

        "obligations": obligations,

        "compliance": compliance,

    }