from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Counsoler, Student, Package
#index route
def index(request):
    
    context = {
        "counsolers": Counsoler.objects.all()
    }

    return render(request, "costcomp/index.html", context)

#for individual counsoler
def counsoler(request, counsoler_id):
    try:
        counsoler = Counsoler.objects.get(pk=counsoler_id)    
    except Counsoler.DoesNotExist:
        raise Http404("Counsoler does not exist")

    context = {
        "counsoler": counsoler,
        "students": counsoler.students.select_related('package').all()
    }

    return render(request, "costcomp/counsoler.html", context)

