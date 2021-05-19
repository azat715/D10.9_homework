from django.shortcuts import render
from django.http import JsonResponse

from core.models import Car

# Create your views here.


def main_view(request):
    if request.method == "GET":
        if request.GET:
            data = list(Car.objects.select_car(request.GET).values())
            return JsonResponse(data, safe=False)
        else:
            return render(request, "car_select.html", {**Car.objects.fields_value()})
