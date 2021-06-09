from django.shortcuts import redirect, render
from .models import Job

# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")

def post_job(request):
    if request.method == "POST":
        Job(user=request.user, title=request.POST["title"], description=request.POST["description"], price=float(request.POST["price"]), quantity=int(request.POST["quantity"])).save()
        return redirect("/")
    return render(request, "dashboard/post-job.html")
