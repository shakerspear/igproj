from django.db import models
from django import forms
from datetime import date,timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


#counsolers
class Counsoler(models.Model):
    #this counsoler level defination affects the Enrollment expressions
    COUNSOLER_LEVEL = (
        ('GC', 'Grauate Coach'),
        ('FAO', 'Former Admissions Officer')
    )

    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    salary = models.IntegerField()
    guaranteed = models.IntegerField()
    level = models.CharField(max_length=3, choices=COUNSOLER_LEVEL, default='GC', blank=False)

    @property
    def total(self): 
        return self.salary + self.guaranteed
    
    def __str__(self):
        return f'{self.level} {self.first} {self.last}'
   

#packages
class Package(models.Model):
    name = models.CharField(max_length=64, unique=True)
    gcHours = models.IntegerField(verbose_name='GC hours')
    faoHours = models.IntegerField(verbose_name='FAO hours')
    courseHours = models.IntegerField(blank=True, null=True)   

    def __str__(self):
        if self.courseHours:
            return f'{self.name}: {self.courseHours} Course Hours, {self.gcHours} GC hours, {self.faoHours} FAO hours'
        else:    
            return f'{self.name}: {self.gcHours} GC hours, {self.faoHours} FAO hours'


#students
class Student(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    def  __str__(self):
        return f'{self.first} {self.last}' 


#to calculate 365 days for default
def enddate_default():      
        return date.today()+timedelta(days=365)
 

def counsolerCost(hourlyCost, packageHours, counsolerStart, counsolerEnd, packageStart, packageEnd):
    '''takes package hours times counsoler span over package span to get how many hours a counsoler get from a package. The hours will times hourly-cost to get a total package cost'''
    
    cost = hourlyCost * packageHours * ((counsolerEnd-counsolerStart)/(packageEnd-packageStart))

    return cost


#enrollment as intermediary
class Enrollment(models.Model):
    GC_Cost = 50    #GC hourly cost
    FAO_Cost = 100   #FAO hourly cost

    students = models.ManyToManyField(Student, related_name='enrollments')
    fao = models.ForeignKey(Counsoler, on_delete=models.PROTECT, related_name='faoEnrollments', limit_choices_to={'level':'FAO'}, blank=True, null=True)
    gc = models.ForeignKey(Counsoler, on_delete=models.PROTECT, related_name='gcEnrollments', limit_choices_to={'level':'GC'}, blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='enrollments')
    packStart = models.DateField(default=date.today, blank=False)  #need enforce endDate no earlier than start
    packEnd = models.DateField(default=enddate_default, blank=False)
    faoStart = models.DateField(default=date.today, blank=True, null=True)
    faoEnd = models.DateField(default=enddate_default, blank=True, null=True)
    gcStart = models.DateField(default=date.today, blank=True, null=True)
    gcEnd = models.DateField(default=enddate_default, blank=True, null=True)
    

    def dateDiff(self, endDate, startDate):
        dateDiff = endDate - startDate
        return dateDiff

    
    def cost(self, counsoler, startDate, endDate):
        '''calculate counsoler's cost for a package. Query dates may not be the full span of the course length'''
        
        packStart = self.packStart
        packEnd = self.packEnd

        if counsoler.level == 'GC':
                        
            if self.gcEnd <= startDate or gcStart >= endDate:
                return 0
            else:
                gcStart = max(self.gcStart, startDate)
                gcEnd = min(self.gcEnd, endDate)
            
            if self.package.courseHours:
                studentCount = self.students.count()
            else:
                studentCount = 1

            hours = self.package.gcHours * studentCount
            cost = counsolerCost(self.GC_Cost, hours, gcStart, gcEnd, packStart, packEnd)
            
            return round(cost,2)
        
        elif counsoler.level == 'FAO':
            if self.package.courseHours:
               courseHours = self.package.courseHours
               studentCount = self.students.count()
            else:
               courseHours = 0
               studentCount = 1

            hours = self.package.faoHours * studentCount + courseHours

            if self.faoEnd <= startDate or self.faoStart >= endDate:
                return 0
            else:
                faoStart = max(self.faoStart, startDate)
                faoEnd = min(self.faoEnd, endDate)
            
            cost = counsolerCost(self.FAO_Cost, hours, faoStart, faoEnd, packStart, packEnd)
            
            return round(cost,2)

    
    def clean(self):
        #enforce the end date is no earlier than start date 
        if self.packStart > self.packEnd:
            raise ValidationError(_('Please set the correct package start and end dates.'))
        
        #make sure there is as least one counsoler
        if self.fao is None and self.gc is None:
            raise ValidationError(_('At least one counsoler needed.'))
        
        #make sure FAO and GC hours will not set, if there isn't matching level counsoler
        if self.fao is None:
            self.faoStart = None
            self.faoEnd = None
        if self.gc is None:
            self.gcStart = None
            self.gcEnd = None

    #optimization can be done here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
    def __str__(self):
        students = self.students.all()
        stuNames = []
        for student in students:
            stuNames.append(student.first)
        names = ', '.join(stuNames)
        return f'{names} enrolled in {self.package}: {self.packStart} to {self.packEnd}'


def startdate_default():
    return date.today()-timedelta(days=365)


#used for period of counsoler performance evaluation
class periodQuery(forms.Form):
    startDate = forms.DateField(initial=startdate_default)
    endDate = forms.DateField(initial=date.today)

    def clean(self):
        endDate = self.cleaned_data["endDate"]
        startDate = self.cleaned_data["startDate"]
        if endDate < startDate:
            raise forms.ValidationError(_('Please enter a valid date.'))
