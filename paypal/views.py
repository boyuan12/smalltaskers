from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def accept_payment_view(request):
    return render(request, "paypal/accept-payment.html")

@csrf_exempt # security issue
def payment_success(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))

        print(post_data)

        return JsonResponse({"success": True})


