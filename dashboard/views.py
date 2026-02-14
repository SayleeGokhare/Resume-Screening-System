from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job, Application
from resumes.models import Resume

@login_required
def dashboard_view(request):
    context = {}
    if request.user.role == 'candidate':
        resume = Resume.objects.filter(user=request.user).first()
        applications = Application.objects.filter(candidate=request.user)
        context['resume'] = resume
        context['applications'] = applications
    elif request.user.role == 'recruiter':
        jobs = Job.objects.filter(recruiter=request.user)
        context['jobs'] = jobs
        
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def my_applications(request):
    applications = Application.objects.filter(candidate=request.user)
    return render(request, 'dashboard/my_applications.html', {'applications': applications})
