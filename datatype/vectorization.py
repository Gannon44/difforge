import numpy as np
import pandas as pd
import umap.umap_ as umap
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import json

class BlockNameVectorizer:
    def __init__(self, csv_path, latent_dim=32):
        """
        Builds a vectorizer for block names using features:
          1. 1 channel of Order-based embedding (normalized index)
          2. 15 channels of Semantic embeddings (using a SentenceTransformer)
          3. 16 channels of TF-IDF embeddings (on block names)
        
        *Old version:*
        Then reduces the concatenated features to a latent_dim vector via UMAP.
        
        Args:
          csv_path: Path to a CSV file containing the ordered block names.
          latent_dim: Target dimension of the latent space.
        """
        self.latent_dim = latent_dim
        df = pd.read_csv(csv_path)
        df = pd.read_csv(csv_path, header=None)  # No headers, treat as unnamed column
        self.block_names = df[0].tolist()  # First column (index 0) contains block names
        self.block_to_latent = self._build_embeddings(self.block_names)
    
    def _build_embeddings(self, block_names):
        n = len(block_names)
        # 1. Positional encoding: normalized index (1 channel)
        order_embeddings = np.array([[i / n] for i in range(n)])  # shape (n, 1)
        
        # 2. LLM embeddings: use SentenceTransformer then reduce to 15 dimensions with UMAP
        model = SentenceTransformer('all-MiniLM-L6-v2')
        semantic_raw = model.encode(block_names, convert_to_numpy=True, show_progress_bar=True)
        umap_sem = umap.UMAP(n_components=15, random_state=42)
        semantic_embeddings = umap_sem.fit_transform(semantic_raw)  # shape (n, 15)
        
        # 3. TF–IDF embeddings: vectorize then reduce to 16 dimensions with UMAP
        tfidf = TfidfVectorizer()
        tfidf_raw = tfidf.fit_transform(block_names).toarray()
        umap_tfidf = umap.UMAP(n_components=16, random_state=42)
        tfidf_embeddings = umap_tfidf.fit_transform(tfidf_raw)  # shape (n, 16)
        
        # Concatenate features: 1 + 15 + 16 = 32 channels
        combined_features = np.hstack([order_embeddings, semantic_embeddings, tfidf_embeddings])
        # Build mapping: block name -> latent vector
        mapping = {name: combined_features[i] for i, name in enumerate(block_names)}
        return mapping

    def transform(self, block_name):
        """
        Returns the latent vector for the given block name.
        If not found, returns a zero vector.
        """
        return self.block_to_latent.get(block_name, np.zeros(self.latent_dim, dtype=np.float32))

    def reverse(self, vector):
        """
        Given a latent vector, finds the closest block name using Euclidean distance.
        """
        best_name = None
        best_dist = float('inf')
        for name, emb in self.block_to_latent.items():
            dist = np.linalg.norm(vector - emb)
            if dist < best_dist:
                best_dist = dist
                best_name = name
        return best_name

if __name__ == '__main__':
    # Example: run once to build and save the mapping dictionaries to JSON files.
    csv_path = "mappings/ordered_block_names.csv"
    vectorizer = BlockNameVectorizer(csv_path, latent_dim=32)
    block_name2latent = {name: emb.tolist() for name, emb in vectorizer.block_to_latent.items()}
    # For a reverse mapping, you might simply invert the dictionary.
    latent2block_name = {str(emb.tolist()): name for name, emb in vectorizer.block_to_latent.items()}
    
    with open("mappings/block_name2latent.json", "w") as f:
        json.dump(block_name2latent, f, indent=2)
    with open("mappings/latent2block_name.json", "w") as f:
        json.dump(latent2block_name, f, indent=2)
    
    print("Vectorizer built and mappings saved.")
    print("Block names -> latent vectors saved to 'mappings/block_name2latent.json'.")
    print("Latent vectors -> block names saved to 'mappings/latent2block_name.json'.")