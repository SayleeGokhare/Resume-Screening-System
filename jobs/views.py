from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm
from django.contrib import messages

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def create_job(request):
    if request.user.role != 'recruiter':
        messages.error(request, "Only recruiters can post jobs.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    if request.user.role != 'candidate':
        messages.error(request, "Only candidates can apply.")
        return redirect('job_list')
        
    job = get_object_or_404(Job, pk=job_id)
    
    # Check if already applied
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_list')

    Application.objects.create(job=job, candidate=request.user)
    messages.success(request, f"Applied to {job.title} successfully.")
    return redirect('dashboard')
