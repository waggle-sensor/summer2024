import gradio as gr
import numpy as np
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_captions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        captions = file.readlines()
    return [caption.strip() for caption in captions]

def semantic_search(query, captions, top_k=5):
    # We first encode the query and captions
    query_embedding = model.encode(query, convert_to_tensor=True)
    caption_embeddings = model.encode(captions, convert_to_tensor=True)
    # Then, we compute cosine similarities
    similarities = util.pytorch_cos_sim(query_embedding, caption_embeddings)[0]
    # Finally, we obtain top_k results
    top_results = np.argsort(-similarities)[:top_k]
    return [(captions[idx], float(similarities[idx])) for idx in top_results]

def search_interface(query):
    captions = load_captions('captions.txt')
    results = semantic_search(query, captions)
    formatted_results = [f"{i}. {caption} (Score: {score:.4f})" for i, (caption, score) in enumerate(results, 1)]
    return "\n".join(formatted_results)

gr.Interface(
    fn=search_interface,
    inputs="text",
    outputs="text",
    title="Semantic Search",
    description="Enter your search query.",
).launch()
