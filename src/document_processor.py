from pathlib import Path
import re



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
        ]
        if any(keyword in line for keyword in skip_keywords):
            continue

        # 3. Skip table data / metadata lines (lines containing tabs or isolated labels)
        if "\t" in line or line.startswith("Paradigm") or line.startswith("Designed by"):
            continue

        # 4. Remove citation brackets (e.g., [1], [2a], [failed verification])
        line = re.sub(r"\[.*?\]", "", line)

        cleaned_lines.append(line)

    # Join the clean lines back together into paragraphs
    return "\n\n".join(cleaned_lines)


def load_document(file_path:str,category:str)->dict:
    
    txt = read_file_content(file_path)
    
    
    
    return{
        "document_id":extract_document_id(file_path),
        "text":clean_wikipedia_text(txt),
        "metadata":{
            "title":f"{extract_document_id(file_path)}.txt",
            "category":category
        }
        
    }
    
    
def fixed_size_chunks(text: str, chunk_size: int, overlap: int) -> list:
    chunks = []
    start = 0
  
    while start < len(text):
        # We will do the text[start:end] slicing in here
        
        chunks.append(text[start:start+chunk_size])
        # Step forward for the next chunk
        start += (chunk_size - overlap) 
        
       
        
    return chunks


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
    text = load_document("data/documents/python.txt", "programming")["text"]

    print("Testing Size 100:")
    chunks_100 = fixed_size_chunks(text, chunk_size=100, overlap=20)
    evaluate_chunks(chunks_100)
    
    
    print("Testing Size 200:")
    chunks_200 = fixed_size_chunks(text, chunk_size=200, overlap=20)
    evaluate_chunks(chunks_200)
        
        
    print("Testing Size 100:")
    chunks_400 = fixed_size_chunks(text, chunk_size=400, overlap=20)
    evaluate_chunks(chunks_400)
    
    
