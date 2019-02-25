from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import *



#index route
def index(request):
    
    context = {
        "counsolers": Counsoler.objects.all()
    }

    return render(request, "costcomp/index.html", context)



#for individual counsoler
def counsoler(request, counsoler_id):
    def costToSalaryDiff(totalCost, queryStart, queryEnd, salaryTotal):
        '''To calculate the cost to salary difference, salary here is yearly cost which will be divided by 365 days to get unit-cost'''
        daysDiff = queryEnd - queryStart
        CSDiff = totalCost - salaryTotal/365*daysDiff.days
        return round(CSDiff, 2)


    try:
        counsoler = Counsoler.objects.get(pk=counsoler_id)    
    except Counsoler.DoesNotExist:
        raise Http404("Counsoler does not exist")
    
   
    #query counsolers performance for a specific period
    if request.method == 'POST':
        form = periodQuery(request.POST)

        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            if counsoler.level == 'FAO':
                enrollments = Enrollment.objects.filter(fao__id=counsoler_id, packStart__lt=endDate, packEnd__gt=startDate)
            elif counsoler.level == 'GC':
                enrollments = Enrollment.objects.filter(gc__id=counsoler_id, packStart__lt=endDate, packEnd__gt=startDate)
            #calculate total cost for certain period of time
            totalCost = 0
            for enrollment in enrollments:
                 totalCost += enrollment.cost(counsoler, startDate, endDate)
            
            CSDiff = costToSalaryDiff(totalCost, startDate, endDate, counsoler.total)

            context = {
                "form": form,
                "counsoler": counsoler,
                "enrollments": enrollments,
                "totalCost": totalCost,
                "CSDiff": CSDiff,
            }

            return render(request, "costcomp/counsoler.html", context)
            
        context = {
            "form": form,
            "counsoler": counsoler,
        }

    else:
        if counsoler.level == 'FAO':
            enrollments =  Enrollment.objects.select_related("package").filter(fao__id=counsoler_id)
        elif counsoler.level == 'GC':
            enrollments =  Enrollment.objects.select_related("package").filter(gc__id=counsoler_id)
        
        form = periodQuery()

        context = {
            "form": form,
            "counsoler": counsoler,
            "enrollments": enrollments,
        }

    return render(request, "costcomp/counsoler.html", context)
    
