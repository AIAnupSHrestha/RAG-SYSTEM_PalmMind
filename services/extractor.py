import io, pathlib
import pdfplumber

def extract_text(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()

    if name.endswith(".pdf"):
        try:
            text_pages = []
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_pages.append(page_text)
            return "\n".join(text_pages)
        except Exception as e:
            print(f"Extraction failed: {e}")
    
    elif name.endswith(".txt"):
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1", errors="ignore")
        
    else:
        return ""
    

if __name__ == "__main__":    
    file_path_str = input("Enter path to PDF or TXT file: ").strip()
    file_path = pathlib.Path(file_path_str)
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
    else:
        with open(file_path, "rb") as f:
            content = f.read()
        
        text = extract_text(content, file_path.name)
        if not text:
            print("No text could be extracted.")
        else:
            print("\nExtracted Text (first 2000 chars):\n")
            print(text[:2000])
