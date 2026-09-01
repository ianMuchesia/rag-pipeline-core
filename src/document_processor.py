from pathlib import Path
import re
import spacy



def extract_document_id(file_path):
    path_obj = Path(file_path)
    
    return path_obj.stem


    
def read_file_content(file_path):
    """Reads a text file and returns its content as a string."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
    
    
def clean_wikipedia_text(raw_text):
    cleaned_lines = []

    for line in raw_text.splitlines():
        line = line.strip()

        # 1. Skip empty lines
        if not line:
            continue

        # 2. Skip navigation text, sidebar labels, and UI elements
        skip_keywords = [
            "hide",
            "Search",
            "Donate",
            "Create account",
            "Log in",
            "Contents",
            "Article",
            "Talk",
            "Read",
            "View source",
            "View history",
            "Main article:",
            "vte",
            "Categories"
        ]
        if any(keyword in line for keyword in skip_keywords):
            continue

        # 3. Skip table data / metadata lines (lines containing tabs or isolated labels)
        if "\t" in line or line.startswith("Paradigm") or line.startswith("Designed by"):
            continue

        # 4. Remove citation brackets (e.g., [1], [2a], [failed verification])
        line = re.sub(r"\[.*?\]", "", line)
        
        if line and line[-1] not in [".","?","!"]:
            line += "."

        cleaned_lines.append(line)

    # Join the clean lines back together into paragraphs
    return "\n\n".join(cleaned_lines)


def clean_with_spacy(wikitext):
    cleaned_lines = []
    nlp = spacy.load("en_core_web_sm")

    # Your raw Wikipedia text variable
    wikipedia_text = wikitext

    # 2. Clean up excess whitespace/newlines before feeding it to spaCy
    # This joins broken lines but keeps text structure clean
    cleaned_text = " ".join(wikipedia_text.split())

    # 3. Process the text
    doc = nlp(cleaned_text)

    # 4. Extract and print only valid, full sentences
    print("--- CLEANED SENTENCE CHUNKS ---\n")
    for sent in doc.sents:
        sentence_string = sent.text.strip()
        
        # Filter out empty strings or random short fragments (like "False" or "{}")
        # A realistic sentence usually has at least 3 words and ends with punctuation
        if len(sentence_string.split()) >= 3 and sentence_string[-1] in [".", "?", "!"]:
            cleaned_lines.append(sentence_string)
            
    return cleaned_lines

def load_document(file_path:str,category:str)->dict:
    
    txt = read_file_content(file_path)
    
    
    
    return{
        "document_id":extract_document_id(file_path),
        "text":clean_with_spacy(clean_wikipedia_text(txt)),
        "metadata":{
            "title":f"{extract_document_id(file_path)}.txt",
            "category":category
        }
        
    }
    
def clean_document(file_path:str,clean_file_path):
    
    
    text = load_document(file_path, "programming")["text"]
    
    
    with open(clean_file_path,"w") as file:
        file.write(" ".join(text))
    
    
    
def fixed_size_chunks(text: str, chunk_size: int, overlap: int) -> list:
    chunks = []
    start = 0
  
    while start < len(text):
        # We will do the text[start:end] slicing in here
        
        chunks.append(text[start:start+chunk_size])
        # Step forward for the next chunk
        start += (chunk_size - overlap) 
        
       
        
    return chunks



def sentence_chunks(sentences: list, max_length: int, overlap_sentences: int) -> list:
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


def evaluate_chunks(chunks):
    chunk_lengths = [len(chunk) for chunk in chunks]
    print(f"Total chunks: {len(chunks)}")
    print(f"Average length: {sum(chunk_lengths) / len(chunk_lengths):.0f} characters")
    print(f"Min length: {min(chunk_lengths)} characters")
    print(f"Max length: {max(chunk_lengths)} characters")
    print("-" * 30)

# The Experiment

# (We would do the same for 200 and 400)

if __name__ == "__main__":
    text = load_document("data/documents/machine_learning.txt", "programming")["text"]
    
    clean_document("data/documents/machine_learning.txt","data/clean_documents/machine_learning.txt")

    
