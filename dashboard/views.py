from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Job, Submission
from paypal.models import UserFund
from django.views.decorators.csrf import csrf_exempt
import boto3
import os
import pathlib
from authentication.models import Profile
from django.contrib.auth.decorators import login_required

s3 = boto3.resource("s3", aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_ID"))


# Create your views here.
@login_required(login_url="/auth/login/")
def index(request):
    jobs = Job.objects.all()
    return render(request, "dashboard/index.html", {
        "jobs": jobs
    })

@login_required(login_url="/auth/login/")
def post_job(request):
    if request.method == "POST":
        uf = UserFund.objects.get(user=request.user)
        if uf.fund < float(request.POST["price"]) * int(request.POST["quantity"]):
            return HttpResponse("Please deposit more money")
        Job(user=request.user, title=request.POST["title"], description=request.POST["description"], price=float(request.POST["price"]), quantity=int(request.POST["quantity"])).save()
        return redirect("/")
    return render(request, "dashboard/post-job.html")

@login_required(login_url="/auth/login/")
def view_task(request, task_id):
    task = Job.objects.get(id=task_id)

    try:
        s = Submission.objects.get(job=task, user=request.user)
        if s.status == "revise":
            return render(request, "dashboard/task.html", {
                "task": task,
                "submission": s
            })
        return HttpResponse("You already submitted a proof, please wait employer to send you a response back. ")
    except Submission.DoesNotExist:
        pass

    if request.method == "POST":
        try:
            s = Submission(user=request.user, job=task, status="revise")
            s.proof = request.POST["proof"]
            s.save()
        except Submission.DoesNotExist:
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

@login_required(login_url="/auth/login/")
def jobs_submitted_tasker(request):
    tasks = Submission.objects.filter(user=request.user)
    return render(request, "dashboard/job-submitted-dashboard.html", {
        "tasks": tasks
    })

@login_required(login_url="/auth/login/")
def cancel_job(request, job_id):
    job = Job.objects.get(id=job_id)
    task = Submission.objects.get(user=request.user, job=job)
    task.delete()
    return redirect("/tasks/")

@login_required(login_url="/auth/login/")
def employer_dashboard(request):
    jobs = Job.objects.filter(user=request.user)
    submissions = []
    for job in jobs:
        submissions.append(Submission.objects.filter(job=job))
    return render(request, "dashboard/employer-dashboard.html", {
        "submissions": submissions
    })

@login_required(login_url="/auth/login/")
def review_submission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    profile = Profile.objects.get(user=submission.user)
    return render(request, "dashboard/submission.html", {
        "submission": submission,
        "profile": profile
    })

@login_required(login_url="/auth/login/")
def employer_submission_failed(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if submission.status == "success" or submission.status == "failed":
        return HttpResponse("You can't modify the status anymore")

    submission.status = "failed"
    submission.save()
    return redirect("/employer-dashboard/")

@login_required(login_url="/auth/login/")
def employer_submission_revise(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if submission.status == "success" or submission.status == "failed":
        return HttpResponse("You can't modify the status anymore")

    submission.status = "revise"
    submission.save()
    return redirect("/employer-dashboard/")

@login_required(login_url="/auth/login/")
def employer_submission_success(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if submission.status == "success" or submission.status == "failed":
        return HttpResponse("You can't modify the status anymore")

    submission.status = "success"
    submission.save()

    worker_fund = UserFund.objects.get(user=submission.user)
    employer_fund = UserFund.objects.get(user=submission.job.user)
    price = submission.job.price

    worker_fund.fund += price
    employer_fund.fund -= price
    worker_fund.save()
    employer_fund.save()

    return redirect("/employer-dashboard/")
