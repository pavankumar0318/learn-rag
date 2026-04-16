import os
from langchain.agents import create_agent
from EmbedService import PDFEmbedService
from Models import Models
from RAGService import RAGService
from tools import (
    calculate_risk,
    check_eligibility,
    get_credit_score,
    get_interest_rate,
    get_loan_details,
    invoke_rag,
)

# ─── Initialise services ───────────────────────────────────────────────────────
pdf_embed_service = PDFEmbedService()
rag_service       = RAGService()
models            = Models()

# ─── Embed all PDFs in ./pdfs at startup ──────────────────────────────────────
PDF_DIR = os.getenv("PDF_DIR", "./pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

for fname in os.listdir(PDF_DIR):
    if fname.lower().endswith(".pdf"):
        fpath = os.path.join(PDF_DIR, fname)
        with open(fpath, "rb") as f:
            file_bytes = f.read()
        print(f"[LoanAgent] Embedding: {fname}")
        pdf_embed_service.save_and_embed(fname, file_bytes)

print("[LoanAgent] All PDFs embedded.")

# ─── Tools ────────────────────────────────────────────────────────────────────
tools = [
    get_loan_details,
    get_credit_score,
    check_eligibility,
    calculate_risk,
    get_interest_rate,
    invoke_rag,
]

# ─── Agent ────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a complete retail loan assistant covering:
- HDFC Home Loan Agreements
- RBI/NBFC Loan Lifecycle & Compliance (KYC, AML, IRACP, NPA rules)
- Retail Loan Origination (eligibility, underwriting, collateral, fees, decisioning)

Strict rules:
- NEVER compute eligibility, FOIR, risk scores, or interest rates yourself.
- ALWAYS call the appropriate tool for every financial decision.
- Use invoke_rag for any policy, compliance, agreement, or document question.
- Combine tool outputs into a clear, structured final answer.
- Be concise and factual. Do not speculate.
"""

agent = create_agent(
    model=models.chatModel(),
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)

# ─── CLI entrypoint ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import ast

    while True:
        query = input("User: ").strip()
        if query.lower() in ("exit", "quit"):
            break

        response = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })

        final_message = response["messages"][-1]
        print("\nAI:", final_message.content)

        for message in response["messages"]:
            if message.__class__.__name__ == "ToolMessage" and message.name == "invoke_rag":
                tool_output = message.content
                if isinstance(tool_output, str):
                    try:
                        tool_output = ast.literal_eval(tool_output)
                    except Exception:
                        continue
                sources = tool_output.get("sources", [])
                if sources:
                    print("\n📚 Sources Referenced:")
                    print("-" * 40)
                    for i, src in enumerate(sources, 1):
                        print(f"  [{i}] File   : {src.get('source', 'N/A')}")
                        print(f"       Page   : {src.get('page', 'N/A')}")
                        print(f"       Snippet: {src.get('snippet', 'N/A')}")
                        print()

        print("-" * 40)