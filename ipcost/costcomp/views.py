from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import *




#index route
def index(request):
    if not request.user.is_authenticated:
        return render(request, "costcomp/login.html", {"message": "Here lies InGeniusPrep counsolers' deepest secrets!"})

    context = {
        "counsolers": Counsoler.objects.all()
    }

    return render(request, "costcomp/index.html", context)

#login view
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "costcomp/login.html", {"message": "Invalid Credential."})


#logout view
def logout_view(request):
    logout(request)
    return render(request, "costcomp/login.html", {"message": "Logged Out."})

#for individual counsoler
def counsoler(request, counsoler_id):
    if not request.user.is_authenticated:
        return render(request, "costcomp/login.html", {"message": None})


    def salaryToCostDiff(totalCost, queryStart, queryEnd, salaryTotal):
        '''To calculate the cost to salary difference, salary here is yearly cost which will be divided by 365 days to get unit-cost'''
        daysDiff = queryEnd - queryStart
        SCDiff = salaryTotal/365*daysDiff.days - totalCost 
        return round(SCDiff, 2)


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
                enrollment.var = enrollment.cost(counsoler, startDate, endDate)
                totalCost += enrollment.var

            SCDiff = salaryToCostDiff(totalCost, startDate, endDate, counsoler.total)
            
            context = {
                "user": request.user,
                "form": form,
                "counsoler": counsoler,
                "enrollments": enrollments,
                "defrayal": round(totalCost, 2),
                "SCDiff": SCDiff,
            }

            return render(request, "costcomp/counsoler.html", context)
            
        context = {
            "user": request.user,
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
            "user": request.user,
            "form": form,
            "counsoler": counsoler,
            "enrollments": enrollments,
        }

    return render(request, "costcomp/counsoler.html", context)
    
