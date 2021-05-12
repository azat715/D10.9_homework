from django.shortcuts import render

from core.models import Car

# Create your views here.


def main_view(request):
    if request.method == "GET":
        if request.GET:
            pass
        else:
            print(Car.objects.fields_value())
            return render(request, "car_select.html", {**Car.objects.fields_value()})
    elif request.method == "POST":
        pass
