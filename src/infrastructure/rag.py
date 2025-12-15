from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

load_dotenv()

# Expanded financial knowledge base (Public Data Portal style)
knowledge_base = [
    "The current average interest rate for savings accounts in Korea is around 3.5%.",
    "For safe investments, government bonds and high-yield savings accounts are recommended.",
    "To analyze consumption patterns, it is important to categorize expenses into fixed and variable costs.",
    "Compound interest is the addition of interest to the principal sum of a loan or deposit.",
    "A diversified portfolio helps reduce risk by spreading investments across various financial instruments.",
    "Tickle recommends saving at least 20% of your monthly income.",
    "Emergency funds should cover at least 3 to 6 months of living expenses.",
    "Youth Hope Savings Account: A tax-free savings account for young adults aged 19-34 with an annual income of 36 million KRW or less. Interest rates up to 6%.",
    "Housing Subscription Savings: A must-have account for purchasing a new home in Korea. Minimum monthly deposit is 20,000 KRW.",
    "ISA (Individual Savings Account): A tax-advantaged account that allows you to manage various financial products like deposits, funds, and stocks in one place.",
    "Credit Score Management: Paying credit card bills on time and keeping utilization below 30% helps improve your credit score.",
    "Jeonse Loan: A loan for the unique Korean housing rental system. Interest rates vary by bank and credit score, typically around 4-5%.",
    "KOSPI vs KOSDAQ: KOSPI lists large companies like Samsung, while KOSDAQ lists smaller, tech-heavy companies.",
    "Inflation Hedging: Gold and real estate are traditional assets used to protect against inflation."
]

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def get_vector_store():
    # In a real app, this would persist to disk
    docs = [Document(page_content=text) for text in knowledge_base]
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(docs)
    
    try:
        db = Chroma.from_documents(texts, embeddings)
        return db
    except Exception as e:
        print(f"RAG Initialization failed: {e}")
        return None

def get_retriever():
    db = get_vector_store()
    if db:
        return db.as_retriever(search_kwargs={"k": 2})
    return None
