import os
import django
import sys
from pathlib import Path

# Setup Django environment
sys.path.append(str(Path.cwd()))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_screening_system.settings')
django.setup()

from resumes.models import Resume
import pypdf
import docx

def backfill_content():
    resumes = Resume.objects.all()
    print(f"Found {resumes.count()} resumes to process.")
    
    for resume in resumes:
        if resume.content:
            print(f"Skipping {resume.id} (content already exists)")
            continue
            
        print(f"Processing {resume.id}: {resume.file.name}")
        text = ""
        try:
            path = resume.file.path
            if resume.file.name.endswith('.pdf'):
                with open(path, 'rb') as f:
                    pdf_reader = pypdf.PdfReader(f)
                    for page in pdf_reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted
            elif resume.file.name.endswith('.docx'):
                doc = docx.Document(path)
                for para in doc.paragraphs:
                    text += para.text
            else:
                # Fallback for text files
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            
            if text:
                resume.content = text
                resume.save()
                print(f"Updated {resume.id} with {len(text)} chars.")
            else:
                print(f"No text extracted for {resume.id}.")
                
        except Exception as e:
            print(f"Error processing {resume.id}: {e}")

if __name__ == '__main__':
    backfill_content()
