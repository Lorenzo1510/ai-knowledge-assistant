from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.services.llm_service import llm_predict


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def get_vectorstore():
    return Chroma(embedding_function=embeddings, persist_directory="data/vectorstore")


def index_document(text: str, doc_id: str):
    db = get_vectorstore()
    chunks = splitter.split_text(text)
    metadatas = [{"doc_id": doc_id, "chunk_id": i} for i in range(len(chunks))]
    db.add_texts(chunks, metadatas=metadatas)
    db.persist()

def query_vectorstore(query: str, k: int = 3):
    db = get_vectorstore()
    results = db.similarity_search(query, k=k)
    if not results:
        return "Nessuna informazione trovata nei documenti caricati."
    context = "\n".join([doc.page_content for doc in results])
    return llm_predict(context, query)
