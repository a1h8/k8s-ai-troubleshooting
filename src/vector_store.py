"""
Module for managing the vector database (cosine/Jaccard)
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from jaccard_index.jaccard import jaccard_index

class VectorStore:
    def __init__(self, vectors, meta):
        self.vectors = vectors  # np.array of embeddings
        self.meta = meta        # list of dicts with metadata

    def query(self, query_vec, top_k=5, threshold=0.73, metric='cosine'):
        """
        Query the vector store using cosine or Jaccard similarity.
        Returns all items above threshold, otherwise top_k results.
        """
        if metric == 'cosine':
            sims = cosine_similarity([query_vec], self.vectors)[0]
        elif metric == 'jaccard':
            sims = np.array([jaccard_index(query_vec, v) for v in self.vectors])
        else:
            raise ValueError('Unknown metric')
        idx = np.where(sims >= threshold)[0]
        if len(idx) == 0:
            idx = np.argsort(sims)[-top_k:]
        return [(self.meta[i], float(sims[i])) for i in idx]
