from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job, Application
from resumes.models import Resume
from .matcher import calculate_match

@login_required
def ranking(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Security check: only the recruiter who posted the job can view rankings
    if request.user != job.recruiter:
        return redirect('dashboard')
        
    applications = Application.objects.filter(job=job)
    results = []

    job_text = f"{job.title} {job.description} {job.required_skills}"

    for app in applications:
        resume = Resume.objects.filter(user=app.candidate).first()
        if resume:
            # Re-read file content or use stored skills/text
            # For efficiency we should store parsed text in Resume model, but for now we iterate
            # We will use resume.skills + any other info
            # We will use resume.content if available (for new uploads), else skills
            resume_content = resume.content if resume.content else resume.skills
            
            score, matched, missing = calculate_match(resume_content, job_text)
            
            # Convert sets to sorted lists for consistent display and slicing support
            matched_list = sorted(list(matched)) if matched else []
            missing_list = sorted(list(missing)) if missing else []
            
            results.append({
                'candidate': app.candidate,
                'score': score,
                'matched': matched_list,
                'missing': missing_list,
                'resume_url': resume.file.url
            })
    
    # Sort by score desc
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return render(request, 'screening/ranking.html', {'job': job, 'results': results})
