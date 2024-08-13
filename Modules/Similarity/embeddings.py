from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoTokenizer, AutoModel
import numpy as np
import torch
import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
import os
import voyageai


os.environ['VOYAGE_API_KEY'] = "YOUR_VOYAGE_API_KEY"
vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"),)

class Embeddings:
    def train_word2vec_model(self, cpp_code):
        # Generate tokens for each code snippet
        tokenized_data = [code.split() for code in cpp_code]
        
        # Train Word2Vec model
        model = Word2Vec(sentences=tokenized_data, vector_size=128, window=5, min_count=1)

        return model
        
    def get_word2vec_embeddings(self, model, code_snippet):
        # Tokenize the code snippet
        tokenized_code = code_snippet.split()

        # Generate embeddings for each word and filter out words not in vocabulary
        embeddings = [model.wv[word] for word in tokenized_code if word in model.wv]

        # Calculate the mean embedding
        if embeddings:
            mean_embedding = np.mean(embeddings, axis=0)
        else:
            None

        return mean_embedding
    
    def train_tfidf_model(self, codes):
        # Stop words in cpp code
        stop_words = ['{', '}', '(', ')', '[', ']', '.', ';', ',', '<<', '>>']
        # Create TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
        tfidf_vectorizer.fit(codes)
        return tfidf_vectorizer

    def get_tfidf_embeddings(self, model, code):
        # Transform code to TF-IDF vectors
        tfidf_matrix = model.transform([code])
        return tfidf_matrix.toarray()
    
    def load_codebert_model(self):
        # Load pre-trained model tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        model = AutoModel.from_pretrained("microsoft/codebert-base")
        return tokenizer, model
    
    def get_codebert_embeddings(self, tokenizer, model, code_snippet):
        inputs = tokenizer(code_snippet, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embeddings
    
    def train_doc2vec_model(self, cpp_code):
        # Tag each code snippet with an index
        tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(cpp_code)]
        
        # Train Doc2Vec model
        model = Doc2Vec(vector_size=128, window=2, min_count=1, workers=4, epochs=40)
        model.build_vocab(tagged_data)
        model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
        
        return model
    
    def get_doc2vec_embeddings(self, model, code_snippet):
        # Tokenize the code snippet
        tokenized_code = word_tokenize(code_snippet.lower())
        
        # Generate the vector for the code snippet
        vector = model.infer_vector(tokenized_code)
        
        return vector
    
    def get_voyage_embeddings(self, code_snippet):        
        embeddings = vo.embed([code_snippet], model="voyage-code-2", input_type="query",truncation=True).embeddings[0]
        return embeddings