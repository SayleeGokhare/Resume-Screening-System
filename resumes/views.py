from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resume
from .parser import extract_skills
import pypdf
import docx
import io

@login_required
def upload_resume(request):
    if request.method == 'POST':
        file = request.FILES['file']
        text = ""
        
        try:
            if file.name.endswith('.pdf'):
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            elif file.name.endswith('.docx'):
                doc = docx.Document(file)
                for para in doc.paragraphs:
                    text += para.text
            else:
                # Fallback for text files
                text = file.read().decode('utf-8')
        except Exception as e:
            print(f"Error reading file: {e}")

        skills = extract_skills(text)

        # Handle existing resumes (cleanup duplicates if any)
        existing_resumes = Resume.objects.filter(user=request.user).order_by('-id')
        if existing_resumes.exists():
            resume = existing_resumes.first()
            # Delete any extra duplicates
            for dup in existing_resumes[1:]:
                dup.delete()
        else:
            resume = Resume(user=request.user)

        resume.file = file
        resume.skills = skills
        resume.content = text
        resume.save()

        return redirect('dashboard')

    return render(request, 'resumes/upload.html')
