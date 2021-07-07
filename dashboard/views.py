from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Job, Submission
from paypal.models import UserFund
from django.views.decorators.csrf import csrf_exempt
import boto3
import os
import pathlib
from authentication.models import Profile

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

    try:
        Submission.objects.get(job=task, user=request.user)
        return HttpResponse("You already submitted a proof, please wait employer to send you a response back. ")
    except Submission.DoesNotExist:
        pass

    if request.method == "POST":
        Submission(user=request.user, job=task, proof=request.POST["proof"]).save()
        return HttpResponse("Proof submitted successfully. If you don't hear a response back within a week, your submission will automatically approved")

    else:
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

def jobs_submitted_tasker(request):
    tasks = Submission.objects.filter(user=request.user)
    return render(request, "dashboard/job-submitted-dashboard.html", {
        "tasks": tasks
    })

def cancel_job(request, job_id):
    job = Job.objects.get(id=job_id)
    task = Submission.objects.get(user=request.user, job=job)
    task.delete()
    return redirect("/tasks/")

def employer_dashboard(request):
    jobs = Job.objects.filter(user=request.user)
    submissions = []
    for job in jobs:
        submissions.append(Submission.objects.filter(job=job))
    return render(request, "dashboard/employer-dashboard.html", {
        "submissions": submissions
    })

def review_submission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    profile = Profile.objects.get(user=submission.user)
    return render(request, "dashboard/submission.html", {
        "submission": submission,
        "profile": profile
    })
