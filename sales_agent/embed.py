from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings

def get_embed():
    embed = HuggingFaceBgeEmbeddings(model_name = "thenlper/gte-large")
    return embed