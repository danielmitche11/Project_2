# from dotenv import load_dotenv
# from langchain.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.huggingface import HuggingFaceEmbeddings
# from langchain.vectorstores import Pinecone

# # # Load environment variables from .env file
# load_dotenv()





# loader = TextLoader("D:\Revature\Project-2\Dataset\Bright_speed_dataset.txt")
# pages = loader.load_and_split()

# embeddings_model = HuggingFaceEmbeddings(
#     model_name="thenlper/gte-large",
#     encode_kwargs={"normalize_embeddings": True},
# )
# text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
# documents = text_splitter.split_documents(pages)

# index= "starter"
# namespace='brightspeed'
# Pinecone.from_documents(documents, embeddings_model, index_name=index,namespace=namespace)











