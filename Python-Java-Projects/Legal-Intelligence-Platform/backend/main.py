from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from pydantic import BaseModel
import io

from analyzer import analyze_contract


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Enterprise Legal Intelligence Platform",
    version="1.0.0",
    description=(
        "AI-powered Legal Document, Contract Risk, "
        "Compliance and Obligation Intelligence API"
    ),
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Enterprise Legal Intelligence Platform API is running!",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Legal Intelligence API",
    }


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file_bytes: bytes):

    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)

        pages = len(reader.pages)
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

        text = "\n".join(text_parts)

        return pages, text

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read PDF: {str(e)}",
        )


# ============================================================
# FILE VALIDATION
# ============================================================

def validate_pdf(file: UploadFile):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )


# ============================================================
# UPLOAD CONTRACT
# ============================================================

@app.post("/contracts/upload")
async def upload_contract(
    file: UploadFile = File(...)
):

    validate_pdf(file)

    file_bytes = await file.read()

    pages, text = extract_pdf_text(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF.",
        )

    return {
        "filename": file.filename,
        "pages": pages,
        "text_length": len(text),
        "text": text,
    }


# ============================================================
# CONTRACT ANALYSIS
# ============================================================

@app.post("/contracts/analyze")
async def analyze_uploaded_contract(
    file: UploadFile = File(...)
):

    validate_pdf(file)

    file_bytes = await file.read()

    pages, text = extract_pdf_text(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF.",
        )

    analysis = analyze_contract(text)

    return {
        "filename": file.filename,
        "pages": pages,
        "text_length": len(text),
        "analysis": analysis,
        "text": text,
    }


# ============================================================
# COMPLIANCE INTELLIGENCE
# ============================================================

@app.post("/compliance/check")
async def compliance_check(
    file: UploadFile = File(...)
):

    validate_pdf(file)

    file_bytes = await file.read()

    pages, text = extract_pdf_text(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF.",
        )

    analysis = analyze_contract(text)

    compliance = analysis.get("compliance", [])

    detected = [
        item
        for item in compliance
        if item.get("status") == "Detected"
    ]

    not_detected = [
        item
        for item in compliance
        if item.get("status") == "Not Detected"
    ]

    compliance_score = (
        round(
            (len(detected) / len(compliance)) * 100
        )
        if compliance
        else 0
    )

    if compliance_score >= 80:
        compliance_status = "Good"
    elif compliance_score >= 50:
        compliance_status = "Needs Review"
    else:
        compliance_status = "High Attention Required"

    return {
        "filename": file.filename,
        "pages": pages,
        "compliance_score": compliance_score,
        "compliance_status": compliance_status,
        "total_frameworks": len(compliance),
        "detected_count": len(detected),
        "not_detected_count": len(not_detected),
        "detected": detected,
        "not_detected": not_detected,
        "compliance": compliance,
    }


# ============================================================
# ALERT CENTER
# ============================================================

@app.post("/alerts/generate")
async def generate_alerts(
    file: UploadFile = File(...)
):

    validate_pdf(file)

    file_bytes = await file.read()

    pages, text = extract_pdf_text(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF.",
        )

    analysis = analyze_contract(text)

    alerts = []

    # Risk alerts
    for risk in analysis.get("risks", []):

        severity = risk.get("severity", "Medium")

        alerts.append({
            "type": "Risk",
            "severity": severity,
            "title": risk.get(
                "risk",
                "Contract Risk",
            ),
            "description": risk.get(
                "explanation",
                "Potential contractual risk detected.",
            ),
        })

    # Missing clause alerts
    for clause in analysis.get("missing_clauses", []):

        alerts.append({
            "type": "Missing Clause",
            "severity": clause.get(
                "severity",
                "Medium",
            ),
            "title": (
                "Missing "
                + clause.get(
                    "clause",
                    "Legal Clause",
                )
                + " Clause"
            ),
            "description": (
                "This legal clause was not detected "
                "in the contract."
            ),
        })

    # Compliance alerts
    for item in analysis.get("compliance", []):

        if item.get("status") == "Not Detected":

            alerts.append({
                "type": "Compliance",
                "severity": "Low",
                "title": (
                    item.get(
                        "framework",
                        "Compliance",
                    )
                    + " Review Required"
                ),
                "description": (
                    "No explicit "
                    + item.get(
                        "framework",
                        "compliance",
                    )
                    + " requirement was detected."
                ),
            })

    priority = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    alerts.sort(
        key=lambda alert: priority.get(
            alert.get("severity"),
            4,
        )
    )

    high_priority = sum(
        1
        for alert in alerts
        if alert.get("severity") == "High"
    )

    medium_priority = sum(
        1
        for alert in alerts
        if alert.get("severity") == "Medium"
    )

    low_priority = sum(
        1
        for alert in alerts
        if alert.get("severity") == "Low"
    )

    return {
        "filename": file.filename,
        "pages": pages,
        "total_alerts": len(alerts),
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
        "alerts": alerts,
    }


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

@app.post("/dashboard/summary")
async def dashboard_summary(
    file: UploadFile = File(...)
):

    validate_pdf(file)

    file_bytes = await file.read()

    pages, text = extract_pdf_text(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF.",
        )

    analysis = analyze_contract(text)

    clauses = analysis.get("clauses", [])
    risks = analysis.get("risks", [])
    obligations = analysis.get("obligations", [])
    missing_clauses = analysis.get("missing_clauses", [])
    compliance = analysis.get("compliance", [])

    high_risks = [
        risk
        for risk in risks
        if risk.get("severity") == "High"
    ]

    compliance_detected = [
        item
        for item in compliance
        if item.get("status") == "Detected"
    ]

    compliance_score = (
        round(
            (
                len(compliance_detected)
                / len(compliance)
            ) * 100
        )
        if compliance
        else 0
    )

    return {
        "filename": file.filename,
        "pages": pages,
        "risk_score": analysis.get(
            "risk_score",
            0,
        ),
        "risk_level": analysis.get(
            "risk_level",
            "Low",
        ),
        "active_clauses": len(clauses),
        "missing_clauses": len(missing_clauses),
        "risks_found": len(risks),
        "high_risks": len(high_risks),
        "obligations": len(obligations),
        "compliance_score": compliance_score,
        "summary": {
            "clauses": clauses,
            "risks": risks,
            "missing_clauses": missing_clauses,
            "obligations": obligations,
            "compliance": compliance,
        },
    }


# ============================================================
# AI LEGAL COPILOT
# ============================================================

class CopilotRequest(BaseModel):
    question: str
    contract_text: str = ""


@app.post("/copilot/ask")
def copilot_ask(request: CopilotRequest):

    question = request.question.strip()
    question_lower = question.lower()
    contract_text = request.contract_text.strip()

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not question:
        return {
            "answer": "Please enter a legal question."
        }

    if not contract_text:
        return {
            "answer": (
                "Please upload and analyze a contract first "
                "so I can answer questions about it."
            )
        }

    # --------------------------------------------------------
    # Run the same intelligence engine
    # --------------------------------------------------------

    analysis = analyze_contract(contract_text)

    risks = analysis.get("risks", [])
    clauses = analysis.get("clauses", [])
    missing = analysis.get("missing_clauses", [])
    obligations = analysis.get("obligations", [])
    compliance = analysis.get("compliance", [])

    risk_score = analysis.get("risk_score", 0)
    risk_level = analysis.get("risk_level", "Low")

    # ========================================================
    # SUMMARY
    # ========================================================

    if (
        "summarize" in question_lower
        or "summary" in question_lower
        or "overview" in question_lower
    ):

        detected_clause_names = [
            item.get("clause")
            for item in clauses
        ]

        high_risks = [
            r for r in risks
            if r.get("severity") == "High"
        ]

        medium_risks = [
            r for r in risks
            if r.get("severity") == "Medium"
        ]

        return {
            "answer": (
                "Contract Summary\n\n"
                f"Risk Level: {risk_level}\n"
                f"Risk Score: {risk_score}/100\n\n"
                f"Detected Clauses: {len(clauses)}\n"
                f"{', '.join(detected_clause_names) if detected_clause_names else 'None'}\n\n"
                f"Risks Found: {len(risks)}\n"
                f"High: {len(high_risks)} | "
                f"Medium: {len(medium_risks)}\n\n"
                f"Missing Clauses: {len(missing)}\n"
                f"Obligations: {len(obligations)}\n\n"
                "Overall Assessment:\n"
                "The contract has been analyzed for clauses, "
                "contractual risks, missing provisions, "
                "obligations and compliance indicators."
            )
        }

    # ========================================================
    # RISKS
    # ========================================================

    if (
        "risk" in question_lower
        or "risky" in question_lower
        or "danger" in question_lower
        or "problem" in question_lower
    ):

        if not risks:
            return {
                "answer": (
                    "No specific contractual risks were detected "
                    "by the current risk engine."
                )
            }

        lines = [
            f"Contract Risk Assessment: {risk_level} ({risk_score}/100)",
            "",
            f"{len(risks)} potential risk(s) were detected:",
            "",
        ]

        for index, risk in enumerate(risks, 1):

            lines.append(
                f"{index}. {risk.get('risk', 'Contract Risk')} "
                f"[{risk.get('severity', 'Medium')}]"
            )

            lines.append(
                f"   {risk.get('explanation', '')}"
            )

            lines.append("")

        return {
            "answer": "\n".join(lines)
        }

    # ========================================================
    # OBLIGATIONS
    # ========================================================

    if (
        "obligation" in question_lower
        or "responsibil" in question_lower
        or "duties" in question_lower
        or "duty" in question_lower
    ):

        if not obligations:
            return {
                "answer": (
                    "No specific contractual obligations "
                    "were extracted from the available text."
                )
            }

        lines = [
            f"{len(obligations)} contractual obligation(s) were identified:",
            "",
        ]

        for index, item in enumerate(obligations[:10], 1):

            obligation = item.get(
                "obligation",
                "",
            )

            lines.append(
                f"{index}. {obligation}"
            )
            lines.append("")

        if len(obligations) > 10:
            lines.append(
                f"...and {len(obligations) - 10} more obligations."
            )

        return {
            "answer": "\n".join(lines)
        }

    # ========================================================
    # MISSING CLAUSES
    # ========================================================

    if (
        "missing" in question_lower
        or "absent" in question_lower
        or "not included" in question_lower
        or "which clauses" in question_lower
    ):

        if not missing:
            return {
                "answer": (
                    "No obvious missing clauses were detected "
                    "by the current clause engine."
                )
            }

        lines = [
            f"{len(missing)} potentially missing clause(s):",
            "",
        ]

        for index, clause in enumerate(missing, 1):

            lines.append(
                f"{index}. {clause.get('clause', 'Legal Clause')} "
                f"[{clause.get('severity', 'Medium')}]"
            )

            lines.append(
                "   This clause was not detected in the contract."
            )

            lines.append("")

        return {
            "answer": "\n".join(lines)
        }

    # ========================================================
    # CLAUSES
    # ========================================================

    if (
        "clause" in question_lower
        or "provision" in question_lower
        or "sections" in question_lower
    ):

        if not clauses:
            return {
                "answer": (
                    "No recognized legal clauses were detected."
                )
            }

        lines = [
            f"{len(clauses)} legal clause(s) were detected:",
            "",
        ]

        for index, clause in enumerate(clauses, 1):

            keywords = clause.get(
                "keywords",
                [],
            )

            lines.append(
                f"{index}. {clause.get('clause', 'Clause')}"
            )

            if keywords:
                lines.append(
                    f"   Keywords: {', '.join(keywords)}"
                )

            lines.append("")

        return {
            "answer": "\n".join(lines)
        }

    # ========================================================
    # COMPLIANCE
    # ========================================================

    if (
        "compliance" in question_lower
        or "regulatory" in question_lower
        or "regulation" in question_lower
        or "gdpr" in question_lower
    ):

        detected = [
            item
            for item in compliance
            if item.get("status") == "Detected"
        ]

        not_detected = [
            item
            for item in compliance
            if item.get("status") == "Not Detected"
        ]

        score = (
            round(
                len(detected)
                / len(compliance)
                * 100
            )
            if compliance
            else 0
        )

        lines = [
            f"Compliance Coverage: {score}%",
            "",
            "Detected:",
        ]

        for item in detected:
            lines.append(
                f"✓ {item.get('framework', 'Framework')}"
            )

        lines.append("")
        lines.append("Not Detected:")

        for item in not_detected:
            lines.append(
                f"! {item.get('framework', 'Framework')}"
            )

        return {
            "answer": "\n".join(lines)
        }

    # ========================================================
    # CONFIDENTIALITY
    # ========================================================

    if (
        "confidential" in question_lower
        or "nda" in question_lower
    ):

        text_lower = contract_text.lower()

        if "confidential" in text_lower:

            return {
                "answer": (
                    "A confidentiality provision is present.\n\n"
                    "The contract requires confidential information "
                    "to be protected and restricts unauthorized disclosure."
                )
            }

        return {
            "answer": (
                "No clear confidentiality provision was detected "
                "in the contract."
            )
        }

    # ========================================================
    # SIMPLE EXPLANATION
    # ========================================================

    if (
        "explain" in question_lower
        or "simple" in question_lower
        or "meaning" in question_lower
    ):

        return {
            "answer": (
                f"In simple terms, this contract defines "
                f"the responsibilities and legal relationship "
                f"between the parties.\n\n"
                f"The current analysis found {len(clauses)} "
                f"legal clauses, {len(risks)} potential risks, "
                f"{len(missing)} potentially missing clauses "
                f"and {len(obligations)} obligations.\n\n"
                f"Overall risk level: {risk_level} "
                f"({risk_score}/100)."
            )
        }

    # ========================================================
    # DEFAULT RESPONSE
    # ========================================================

    return {
        "answer": (
            "I analyzed the current contract. You can ask me:\n\n"
            "• Summarize this contract\n"
            "• What are the risks?\n"
            "• What obligations exist?\n"
            "• Which clauses are missing?\n"
            "• What clauses were detected?\n"
            "• What is the compliance status?\n"
            "• Explain the confidentiality clause"
        )
    }