from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]


    else:
        return render(request, "authentication/register.html")
