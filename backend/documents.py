from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

COLLECTION_NAME = "pdf_rag"
PERSIST_DIR = "./chroma_db"

def loadPDF(fileName : str, embeddings):
    '''Loads the PDF into Chroma and returns the vector store'''
    # Initialize the vector store
    vectorStore = Chroma(collection_name=COLLECTION_NAME, embedding_function=embeddings, persist_directory=PERSIST_DIR)

    # If the PDF has already been processed, return the vector store
    check = vectorStore.get(where={"id" : fileName}, limit=1)
    if check["ids"]:
        print("Found vectorized chunks for PDF!")
        return vectorStore
    
    # Else, load the PDF document
    print(f"Loading PDF document {fileName}...")
    loader = PyPDFLoader(fileName)
    document = loader.load()

    # Split the document into chunks.
    print("Splitting the document into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    chunks = splitter.split_documents(document)
    print(f"Splitted document into {len(chunks)} chunks.")

    # Store the chunks on disk
    print("Storing the chunks...")
    for chunk in chunks:
        chunk.metadata["id"] = fileName
    vectorStore.add_documents(chunks)
    print("All chunks stored.")

    return vectorStore