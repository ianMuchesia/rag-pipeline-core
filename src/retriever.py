import numpy as np
import uuid

class VectorRetriever:
    def __init__(self, model):
        self.model = model
        self.chunk_dicts = [] 
        
    def calculate_cosine_similarity(self, A, B):
        return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))
    
        
    def fixed_size_chunks(self,text: str, chunk_size: int, overlap: int) -> list:
        chunks = []
        start = 0
    
        while start < len(text):
            # We will do the text[start:end] slicing in here
            
            chunks.append(text[start:start+chunk_size])
            # Step forward for the next chunk
            start += (chunk_size - overlap) 
            
        
            
        return chunks



    def sentence_chunks(self,sentences: list, max_length: int, overlap_sentences: int) -> list:
        final_chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_len = len(sentence)
            
            # Check if adding this sentence exceeds the limit
            if current_length + sentence_len > max_length and current_chunk:
                # Seal the box
                chunk_text = " ".join(current_chunk)
                final_chunks.append(chunk_text)
                
                # Carry over the overlap
                overlap = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
                current_chunk = overlap + [sentence]
                
                # Recalculate length (+1 for spaces)
                current_length = sum(len(s) + 1 for s in current_chunk) 
                
            else:
                # Keep packing the box
                current_chunk.append(sentence)
                current_length += sentence_len + 1 
                
        # Flush the final remaining sentences
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            final_chunks.append(chunk_text)
            
        return final_chunks


    def semantic_chunks(self, sentences, threshold=0.75):
        prev_embedding = None
        current_chunk = []
        chunks = [] 
        
        for sentence in sentences:
            current_embedding = self.model.encode(sentence)
            
            if prev_embedding is None:
                current_chunk.append(sentence)
                prev_embedding = current_embedding
                continue
                
            if self.calculate_cosine_similarity(current_embedding, prev_embedding) >= threshold:
                current_chunk.append(sentence)
                prev_embedding = current_embedding
            else:
                chunks.append(current_chunk)
                current_chunk = [sentence]
                prev_embedding = current_embedding
                
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks
 
    def index_chunks(self, chunks,source_document):
        
        
        start_index = len(self.chunk_dicts)
        
        for index,chunk in enumerate(chunks):
            
            if isinstance(chunk,list):
                chunk_text = " ".join(chunk)
            else:
                chunk_text = chunk
                
            chunk_embedding = self.model.encode(chunk_text)
            
            chunk_dict = {
                "chunk_id": f"{start_index+index}",
                "text": chunk_text,
                "embedding": chunk_embedding,
                "source_document":source_document
            }
            self.chunk_dicts.append(chunk_dict) 
            
            
            
        
    def search(self, query_text, k=2):
        query_embedding = self.model.encode(query_text)
        
        results = []
       
        for chunk_dict in self.chunk_dicts:
            score = self.calculate_cosine_similarity(query_embedding, chunk_dict["embedding"])
            
            results.append({
                "text": chunk_dict["text"],
                "score": score
            })
            
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
        return sorted_results[:k]