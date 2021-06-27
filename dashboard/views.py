from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Job
from paypal.models import UserFund
from django.views.decorators.csrf import csrf_exempt
import boto3
import os
import pathlib

s3 = boto3.resource("s3", aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_ID"))


# Create your views here.
def index(request):
    jobs = Job.objects.all()
    return render(request, "dashboard/index.html", {
        "jobs": jobs
    })

def post_job(request):
    if request.method == "POST":
        uf = UserFund.objects.get(user=request.user)
        if uf.fund < float(request.POST["price"]) * int(request.POST["quantity"]):
            return HttpResponse("Please deposit more money")
        Job(user=request.user, title=request.POST["title"], description=request.POST["description"], price=float(request.POST["price"]), quantity=int(request.POST["quantity"])).save()
        return redirect("/")
    return render(request, "dashboard/post-job.html")

def view_task(request, task_id):
    task = Job.objects.get(id=task_id)
    return render(request, "dashboard/task.html", {
        "task": task
    })

@csrf_exempt
def file_upload_backend(request):
    import string
    import random
    name = "".join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
    s3.Bucket('smalltasker').put_object(Key=f"{name}{pathlib.Path(request.FILES['file'].name).suffix}", Body=request.FILES["file"], ACL="public-read")
    return JsonResponse({"url": f"https://smalltasker.s3.us-west-1.amazonaws.com/{name}{pathlib.Path(request.FILES['file'].name).suffix}"})

