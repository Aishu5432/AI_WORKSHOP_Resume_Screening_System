from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_store(texts):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.create_documents(texts)

    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="chroma_db"
    )

    return db

def retrieve_documents(query):

    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    docs = db.similarity_search(
        query,
        k=3
    )

    return docs