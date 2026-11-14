from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io

from analyzer import analyze_contract


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Enterprise Legal Intelligence Platform",
    version="1.0.0",
    description=(
        "AI-powered Legal Document, Contract "
        "Risk, Compliance and Obligation Intelligence API"
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

    # Run Contract Intelligence Engine
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

    compliance = analysis.get(
        "compliance",
        [],
    )

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
            (len(detected) / len(compliance))
            * 100
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

    # --------------------------------------------------------
    # Risk Alerts
    # --------------------------------------------------------

    for risk in analysis.get("risks", []):

        severity = risk.get(
            "severity",
            "Medium",
        )

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


    # --------------------------------------------------------
    # Missing Clause Alerts
    # --------------------------------------------------------

    for clause in analysis.get(
        "missing_clauses",
        [],
    ):

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
            ),
            "description": (
                "This legal clause was not detected "
                "in the contract."
            ),
        })


    # --------------------------------------------------------
    # Compliance Alerts
    # --------------------------------------------------------

    for item in analysis.get(
        "compliance",
        [],
    ):

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


    # --------------------------------------------------------
    # Sort Alerts
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Alert Counts
    # --------------------------------------------------------

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
# EXECUTIVE DASHBOARD DATA
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

    clauses = analysis.get(
        "clauses",
        [],
    )

    risks = analysis.get(
        "risks",
        [],
    )

    obligations = analysis.get(
        "obligations",
        [],
    )

    missing_clauses = analysis.get(
        "missing_clauses",
        [],
    )

    compliance = analysis.get(
        "compliance",
        [],
    )

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
            )
            * 100
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

        "missing_clauses": len(
            missing_clauses
        ),

        "risks_found": len(risks),

        "high_risks": len(
            high_risks
        ),

        "obligations": len(
            obligations
        ),

        "compliance_score": compliance_score,

        "summary": {
            "clauses": clauses,
            "risks": risks,
            "missing_clauses": missing_clauses,
            "obligations": obligations,
            "compliance": compliance,
        },
    }