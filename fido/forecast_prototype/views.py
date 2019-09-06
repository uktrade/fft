from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt


def forecast_view(request):
    return render(
        request,
        'forecast_prototype/forecast.html',
    )
