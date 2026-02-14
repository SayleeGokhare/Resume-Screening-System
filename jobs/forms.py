from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'required_skills', 'location', 'job_type', 'salary']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'required_skills': forms.TextInput(attrs={'placeholder': 'Python, Django, SQL (comma separated)'}),
            'location': forms.TextInput(attrs={'placeholder': 'Remote, New York, etc.'}),
            'salary': forms.TextInput(attrs={'placeholder': '$100,000 - $120,000'}),
        }
