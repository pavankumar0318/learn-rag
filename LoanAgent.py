from ast import mod

from langchain.agents import create_agent
# from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from streamlit import pdf
from EmbedService import PDFEmbedService
from Models import Models
from RAGService import RAGService   

from tools import calculate_risk, check_eligibility, get_credit_score, get_interest_rate, get_loan_details, invoke_rag

pdf_embed_service = PDFEmbedService()
ragService = RAGService()

models = Models()

tools = [
    get_loan_details,
    get_credit_score,
    check_eligibility,
    calculate_risk,
    get_interest_rate,
    invoke_rag
]

# RAGService.embed_and_store()

# loader = PyPDFLoader("/Users/pavan/workSpace/learn-rag/pdfs/HDFC_Home_Loan_Agreement.pdf")
file_path = "/Users/pavan/workSpace/learn-rag/pdfs/HDFC_Home_Loan_Agreement.pdf"
with open(file_path, "rb") as f:
    file_bytes = f.read()

doc_id = pdf_embed_service.save_and_embed(
    "HDFC_Home_Loan_Agreement.pdf",
    file_bytes
)  # Simulate PDF upload and embedding

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0
# )

agent = create_agent(
    model=models.chatModel(),
    tools=tools,
    system_prompt="""
You are a financial loan assistant.

Strict rules:
- NEVER calculate eligibility, FOIR, risk, or interest yourself
- ALWAYS call tools for financial decisions
- Use ragService.invoke_rag only for explaining policies or agreements
- Combine tool outputs into a structured final answer
- Be concise and factual
"""
)

if __name__ == "__main__":
    while True:
        query = input("User: ")

        if query.lower() == "exit":
            break

        response = agent.invoke({
            "messages": [
                {"role": "user", "content": query}
            ]
        })

        # Print the AI's final answer
        final_message = response["messages"][-1]
        print("\nAI:", final_message.content)

        # Walk through all messages to find tool results from invoke_rag
        for message in response["messages"]:
            # ToolMessage carries the output of a tool call
            if message.__class__.__name__ == "ToolMessage" and message.name == "invoke_rag":
                tool_output = message.content

                # tool_output may be a string repr of dict — safely eval it
                if isinstance(tool_output, str):
                    import ast
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