from langchain.tools import tool
from regex import T

from RAGService import RAGService


ragService = RAGService()
# --- MOCK DATA LAYER ---

@tool
def get_loan_details(user_id: str) -> dict:
    """Get user's existing loan details including EMI and outstanding amount"""
    return {
        "total_outstanding": 250000,
        "emi": 12000
    }


@tool
def get_credit_score(user_id: str) -> dict:
    """Get user's credit score using user_id"""
    return {
        "score": 742
    }


@tool
def check_eligibility(user_id: str, income: float) -> dict:
    """Check loan eligibility based on user's income, existing EMI, and credit score"""

    loan = get_loan_details.func(user_id=user_id)   # type: ignore # ✅ FIX
    credit = get_credit_score.func(user_id=user_id) # type: ignore # ✅ FIX

    emi = loan["emi"]
    credit_score = credit["score"]

    foir = emi / income

    eligible = foir < 0.5 and credit_score > 650

    return {
        "eligible": eligible,
        "foir": round(foir, 2),
        "credit_score": credit_score,
        "max_loan_amount": income * 10 if eligible else 0
    }


@tool
def calculate_risk(user_id: str, income: float) -> dict:
    """Calculate risk score based on user's credit score and FOIR"""

    loan = get_loan_details.func(user_id=user_id)   # type: ignore # ✅ FIX
    credit = get_credit_score.func(user_id=user_id) # type: ignore # ✅ FIX

    emi = loan["emi"]
    credit_score = credit["score"]

    foir = emi / income

    risk_score = (700 - credit_score)/1000 + foir

    if risk_score < 0.3:
        level = "LOW"
    elif risk_score < 0.6:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": level
    }


@tool
def get_interest_rate(user_id: str, income: float) -> dict:
    """Get loan interest rate based on user's risk level"""

    risk = calculate_risk.func(   # ✅ FIX # type: ignore
        user_id=user_id,
        income=income
    )

    rates = {
        "LOW": 10.5,
        "MEDIUM": 12.0,
        "HIGH": 14.5
    }

    return {
        "risk_level": risk["risk_level"],
        "interest_rate": rates.get(risk["risk_level"], 15.0)
    }

@tool
def invoke_rag(query: str) -> dict:
    """Invoke RAG to answer a query based on embedded PDF content."""
    # This is a placeholder. The actual implementation will call the RAGService.
    # return {
    #     "answer": "This is a simulated RAG response based on the embedded PDF content."
    # }
    return ragService.invoke_rag(query)