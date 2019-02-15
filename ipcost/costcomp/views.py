from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import *



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
    
    enrollments =  Enrollment.objects.select_related("package").filter(counsoler__id=counsoler_id)
    
    totalCost = 0
    for enrollment in enrollments:
        dateDiff = enrollment.endDate.month - enrollment.startDate.month
        totalCost += enrollment.cost

    context = {
        "counsoler": counsoler,
        "enrollments": enrollments,
        "totalcost": totalCost,
        "datediff": dateDiff,
        "costsalad": totalCost-counsoler.total,
    }

    return render(request, "costcomp/counsoler.html", context)

