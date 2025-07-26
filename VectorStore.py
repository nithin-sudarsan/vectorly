from utils import cosine_similarity
import numpy as np
import pandas as pd

class VectorStore:
    def __init__(self):
        self.vector_data = {}
        self.vector_index = {}
    
    def get_vocab(self, phrases: list[str]):
        vocab = set()
        for phrase in phrases:
            tokens = phrase.lower().split()
            vocab.update(tokens)
        return sorted(vocab)
    
    def get_vector(self, phrases, query:str):
        vocab = self.get_vocab(phrases)
        vocab_dict = {word: i for i, word in enumerate(vocab)}
        query_vector = np.zeros(len(vocab))
        query_tokens = query.lower().split()
        for token in query_tokens:
            if token in vocab_dict:
                query_vector[vocab_dict[token]] += 1
        return query_vector

    
    def get_phrase_vector(self, vocab: set, phrases: list[str]):
        vocab_dict = {word: i for i, word in enumerate(vocab)}
        phrase_vector = {}
        for phrase in phrases:
            tokens = phrase.lower().split()
            vector = np.zeros(len(vocab))
            for token in tokens:
                vector[vocab_dict[token]] += 1
            phrase_vector[phrase] = vector
        return phrase_vector
    
    def add_vector(self, vector_id, vector):
        self.vector_data[vector_id] = vector
        # self._update_index(vector_id, vector)
    
    def _update_index(self, vector_id, vector):
        for existing_id, existing_vector in self.vector_data.items():
            similarity = cosine_similarity(vector, existing_vector)
            if existing_id not in self.vector_index:
                self.vector_index[existing_id] = {}
            self.vector_index[existing_id][vector_id] = similarity
    
    def find_similar_vectors(self, query_vector, num_results = 3):
        if len(self.vector_data) > 0:
            if num_results > len(self.vector_data):
                num_results = max(num_results, len(self.vector_data))
        else:
            num_results = 0
        results = []
        for vector_id, vector in self.vector_data.items():
            similarity = cosine_similarity(query_vector, vector)
            results.append((vector_id, similarity))
        results.sort(key = lambda x: x[1], reverse=True)
        return results[:num_results]
    
    def view_similarity_matrix(self):
        phrases = list(self.vector_data.keys())
        similarity_matrix = pd.DataFrame(index=phrases, columns=phrases)

        for sentence, similarities in self.vector_index.items():
            for other_sentence, similarity_score in similarities.items():
                similarity_matrix.loc[sentence, other_sentence] = similarity_score
                similarity_matrix.loc[other_sentence, sentence] = similarity_score
        print(similarity_matrix)