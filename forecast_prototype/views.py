from django.shortcuts import render


def forecast_view(request):
    return render(request, "forecast_prototype/forecast.html")
