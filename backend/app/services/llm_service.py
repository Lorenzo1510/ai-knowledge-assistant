from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def llm_predict(context: str, question: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """
    Rispondi alla domanda in base al seguente contesto:
    {context}

    Domanda: {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    final_prompt = prompt.format(context=context, question=question)
    response = llm.predict(final_prompt)
    print("AAAAAAAAAAAAAAAAAAAAAAA")
    return response
