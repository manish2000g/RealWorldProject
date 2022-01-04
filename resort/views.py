from django.shortcuts import render
from .models import Activity_Type,Activity



def home(request):
    activity_types =Activity_Type.objects.all().order_by('-id')
    context = {
        'activity_types': activity_types,
    }
    return render(request, 'resort/home.html', context)
