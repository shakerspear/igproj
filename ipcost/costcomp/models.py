from django.db import models
from datetime import date,timedelta

#counsolers
class Counsoler(models.Model):
    COUNSOLER_LEVEL = (
        ('GC', 'Grauate Coach'),
        ('FAO', 'Former Admissions Officer')
    )

    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    salary = models.IntegerField()
    guaranteed = models.IntegerField()
    level = models.CharField(max_length=3, choices=COUNSOLER_LEVEL, default='GC')

    @property
    def total(self): 
        return self.salary + self.guaranteed
    
    def __str__(self):
        return f'{self.firstName} {self.lastName} Total:{self.total} = Salary:{self.salary} + Guaranteed:{self.guaranteed}'




def enddate_default():
        return date.today()+timedelta(days=365)
    
#packages
class Package(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    GC_hours = models.IntegerField()
    FAO_hours = models.IntegerField()
    startDate = models.DateField(default=date.today, blank=False)  #need enforce endDate no earlier than start
    endDate = models.DateField(default=enddate_default, blank=False)
   
    @property
    def dateDiff(self):
        dateDiff = self.endDate - self.startDate
        return dateDiff.days


    def __str__(self):
        return f'{self.name}: ${self.price} for {self.dateDiff} days with {self.GC_hours} GC hours and {self.FAO_hours} FAO hours'


#students
class Student(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    counsolers = models.ManyToManyField(Counsoler, through='Enrollment') 
    def  __str__(self):
        return f'{self.firstName} {self.lastName}' 



#enrollment as intermediary
class Enrollment(models.Model):
    GC_Cost = 50    #GC hourly cost
    FAO_Cost = 100   #FAO hourly cost

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollment')
    counsoler = models.ForeignKey(Counsoler, on_delete=models.CASCADE, related_name='enrollment')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='enrollment')
    startDate = models.DateField(default=date.today, blank=False)  #need enforce endDate no earlier than start
    endDate = models.DateField(default=enddate_default, blank=False)
    
    @property
    def dateDiff(self):
        dateDiff = self.endDate - self.startDate
        return dateDiff.days

    @property
    def cost(self):
        if self.counsoler.level == 'GC':
            cost = self.GC_Cost * self.package.GC_hours * (self.dateDiff/self.package.dateDiff)
            return round(cost,2)  #enforce length type calculated with dateDiff
        elif self.counsoler.level == 'FAO':
            cost = self.FAO_Cost * self.package.FAO_hours * (self.dateDiff/self.package.dateDiff)
            return round(cost,2)
    
    def __str__(self):
        return f'{self.student} has enrolled in {self.package}: {self.startDate} to {self.endDate} with {self.counsoler.firstName}'
