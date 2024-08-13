import faiss
import json

from sentence_transformers import SentenceTransformer

class DocumentSearch:
    def __init__(self, dataframe):
        self.df = dataframe
        self.embedding_model = None
        self.index = None
        self.load_model()
        self.load_faiss_index()

    def load_model(self, directory="problems_similarity_dump/mpnet_embedding_model"):
        self.embedding_model = SentenceTransformer(directory)

    def load_faiss_index(self, file_path="problems_similarity_dump/mpnet_faiss_index.bin"):
        self.index = faiss.read_index(file_path)

    def query(self, query_text, k=10):
        query_embedding = self.embedding_model.encode([query_text], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, k)  # D: distances, I: indices
        results = []
        for i, idx in enumerate(I[0]):
            problem_text = self.df.iloc[idx]['problem_statement']
            problem_link = self.df.iloc[idx]['problem_link']
            similarity = D[0][i]
            formatted_similarity = f"{similarity:.2%}"  # Format similarity to percentage with 2 decimals
            results.append({
                "problem_statement": problem_text,
                "problem_link": problem_link,
                "similarity": formatted_similarity
            })
        return json.dumps(results, indent=4)  # Returns JSON string formatted with 4 spaces