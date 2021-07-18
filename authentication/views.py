from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Profile


# Create your views here.
@csrf_exempt
def api_ip(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        request.session["ip_addr"] = post_data["ip"]
        return JsonResponse({"success": True})


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        username = request.POST["username"]
        ip = request.session["ip_addr"]

        try:
            Profile.objects.get(ip=ip)
            return HttpResponse("IP address already used. Try to forgot password if necessary")
        except Profile.DoesNotExist:
            pass

        User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name, password=password)
        user = User.objects.get(username=email)
        Profile(user=user, ip=ip, member_username=username).save()

        login(request, user)

        return HttpResponse("Welcome!")
    else:
        return render(request, "authentication/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("/")
        return HttpResponse("Invalid credentials")

    else:
        return render(request, "authentication/login.html")

def logout_view(request):
    logout(request)
    return redirect("/auth/login")
