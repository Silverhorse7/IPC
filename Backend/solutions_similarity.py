import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import voyageai

os.environ['VOYAGE_API_KEY'] = "YOUR_VOYAGE"
vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))

class CodeSearch:
    def __init__(self, dataframe):
        self.df = dataframe
        self.embedding_model = None
        self.index = None

    def load_faiss_index(self, file_path="solutions_similarity_dump/voyage_faiss_index.bin"):
        self.index = faiss.read_index(file_path)

    def query(self, query_code, k=10):
        query_embedding = np.array(vo.embed([query_code], model="voyage-code-2", input_type="query").embeddings, dtype=float)
        D, I = self.index.search(query_embedding, k)  # D: distances, I: indices
        results = []
        for i, idx in enumerate(I[0]):
            solution = self.df.iloc[idx]['solution']
            problem_link = self.df.iloc[idx]['problem_link']
            similarity = D[0][i]
            formatted_similarity = f"{similarity:.2%}"  # Format similarity to percentage with 2 decimals
            results.append({
                "problem_link": problem_link,
                "solution": solution,
                "similarity": formatted_similarity
            })
        return json.dumps(results, indent=4)  # Returns JSON string formatted with 4 spacesq