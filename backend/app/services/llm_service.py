import os
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceEndpoint

hg_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def llm_predict(context: str, question: str) -> str:
    template = """
    Rispondi alla domanda in base al seguente contesto:
    {context}

    Domanda: {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    final_prompt = prompt.format(context=context, question=question)

    llm = HuggingFaceEndpoint(
        endpoint_url="https://api-inference.huggingface.co/models/google/flan-t5-large",
        huggingfacehub_api_token=hg_api_token,
        temperature=0.7,
        max_length=512
    )
    
    return llm.predict(final_prompt)
