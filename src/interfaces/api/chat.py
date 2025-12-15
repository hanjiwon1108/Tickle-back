from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from src.domain import models
from src.infrastructure import auth
from src.interfaces.api.auth import get_current_user
from src.infrastructure.database import get_db
from src.infrastructure.rag import get_retriever

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.7)
retriever = get_retriever()

template = """You are Tickle, a friendly and helpful AI financial advisor. 
Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Keep your answers concise and encouraging.

IMPORTANT: Always format your responses using Markdown for better readability:
- Use **bold** for emphasis on important terms
- Use bullet points or numbered lists when listing items
- Use headers (##, ###) for organizing longer responses
- Use `code` formatting for numbers, percentages, or specific values
- Use > blockquotes for tips or important notes

Context: {context}

Question: {question}

Answer (in Markdown format):"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

qa_chain = None
if retriever:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # In a real app, we would save the chat history here
    try:
        if qa_chain:
            response = qa_chain.run(request.message)
        else:
            # Fallback to direct LLM call if RAG is not available
            # We need to construct a prompt manually since we don't have the chain
            fallback_prompt = f"""You are Tickle, a friendly and helpful AI financial advisor.
            
IMPORTANT: Always format your responses using Markdown for better readability:
- Use **bold** for emphasis on important terms
- Use bullet points or numbered lists when listing items
- Use headers (##, ###) for organizing longer responses
- Use `code` formatting for numbers, percentages, or specific values

Question: {request.message}

Answer (in Markdown format):"""
            msg = llm.invoke(fallback_prompt)
            response = msg.content
            
        return {"response": response}
    except Exception as e:
        error_message = str(e)
        if "429" in error_message or "quota" in error_message.lower():
            raise HTTPException(
                status_code=503, 
                detail="AI 서비스가 일시적으로 사용량 한도에 도달했습니다. 잠시 후 다시 시도해주세요."
            )
        raise HTTPException(status_code=500, detail=error_message)
