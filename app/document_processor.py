import os
import fitz  # PyMuPDF
import docx2txt
import email
from bs4 import BeautifulSoup
from typing import List
from email import policy
from email.parser import BytesParser


class DocumentProcessor:
    def __init__(self, chunk_size=300, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def load_pdf(self, path: str) -> str:
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])

    def load_docx(self, path: str) -> str:
        return docx2txt.process(path)

    def load_eml(self, path: str) -> str:
        with open(path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        body = msg.get_body(preferencelist=('plain', 'html'))
        if body.get_content_type() == 'text/html':
            return BeautifulSoup(body.get_content(), 'html.parser').get_text()
        return body.get_content()

    def extract_text(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return self.load_pdf(file_path)
        elif ext == '.docx':
            return self.load_docx(file_path)
        elif ext == '.eml':
            return self.load_eml(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)
        return chunks
