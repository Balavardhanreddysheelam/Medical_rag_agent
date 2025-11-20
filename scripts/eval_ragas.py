import os
import asyncio
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_precision,
    context_recall,
)
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# You need to set GROQ_API_KEY in env
# And potentially OPENAI_API_KEY if using default Ragas metrics with OpenAI, 
# but we will try to configure it to use Groq if possible or just warn user.

# Note: Ragas default metrics often rely on OpenAI. 
# Configuring Ragas to use other LLMs requires passing `llm` and `embeddings` to the metrics.

async def main():
    print("Starting RAGAS evaluation...")
    
    # 1. Define sample questions and ground truths
    questions = [
        "What is John Doe's chief complaint?",
        "What is the plan for Jane Smith?",
    ]
    
    ground_truths = [
        ["Chest pain."],
        ["Ibuprofen 400mg. Follow up with Dr. House."],
    ]
    
    # 2. Get answers and contexts from our RAG agent
    # In a real script, we would call our API or use the service directly.
    # Here we mock the retrieval for demonstration or import the service if env is set.
    
    # Mocking for now as we need the backend running to query real data
    answers = [
        "John Doe's chief complaint is chest pain.",
        "The plan for Jane Smith is Ibuprofen 400mg and follow up with Dr. House.",
    ]
    
    contexts = [
        ["Patient Name: [REDACTED]\nChief Complaint: Chest pain."],
        ["Plan: Ibuprofen 400mg. Follow up with Dr. [REDACTED]."],
    ]
    
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    dataset = Dataset.from_dict(data)
    
    # 3. Evaluate
    # We need to pass the LLM to use for evaluation if not OpenAI
    # For simplicity in this scaffold, we assume OpenAI or compatible env is set for Ragas
    
    try:
        results = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevance,
            ],
        )
        print(results)
    except Exception as e:
        print(f"Evaluation failed (likely due to missing OpenAI key for Ragas default): {e}")
        print("To fix, export OPENAI_API_KEY or configure Ragas with Groq LLM.")

if __name__ == "__main__":
    asyncio.run(main())
