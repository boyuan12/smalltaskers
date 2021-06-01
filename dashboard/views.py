from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")

def post_job(request):
    return render(request, "dashboard/post-job.html")
