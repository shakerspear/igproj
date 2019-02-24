from django.db import models
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



#to calculate 365 days for default
def enddate_default():      
        return date.today()+timedelta(days=365)
    

#packages
class Package(models.Model):
    name = models.CharField(max_length=64, unique=True)
    gcHours = models.IntegerField(verbose_name='GC hours')
    faoHours = models.IntegerField(verbose_name='FAO hours')
    courseHours = models.IntegerField(blank=True, null=True)   

    def __str__(self):
        if self.courseHours:
            return f'{self.name}: {self.courseHours} Course Hours {self.gcHours} GC hours {self.faoHours} FAO hours'
        else:    
            return f'{self.name}: {self.gcHours} GC hours {self.faoHours} FAO hours'


#students
class Student(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    def  __str__(self):
        return f'{self.first} {self.last}' 



#enrollment as intermediary
class Enrollment(models.Model):
    GC_Cost = 50    #GC hourly cost
    FAO_Cost = 100   #FAO hourly cost

    students = models.ManyToManyField(Student, related_name='enrollments')
    fao = models.ForeignKey(Counsoler, on_delete=models.CASCADE, related_name='faoEnrollments', limit_choices_to={'level':'FAO'}, blank=True, null=True)
    gc = models.ForeignKey(Counsoler, on_delete=models.CASCADE, related_name='gcEnrollments', limit_choices_to={'level':'GC'}, blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='enrollments')
    packStart = models.DateField(default=date.today, blank=False)  #need enforce endDate no earlier than start
    packEnd = models.DateField(default=enddate_default, blank=False)
    faoStart = models.DateField(default=date.today, blank=True, null=True)
    faoEnd = models.DateField(default=enddate_default, blank=True, null=True)
    gcStart = models.DateField(default=date.today, blank=True, null=True)
    gcEnd = models.DateField(default=enddate_default, blank=True, null=True)
    

    def dateDiff(self, endDate, startDate):
        dateDiff = endDate - startDate
        return dateDiff

    @property
    def cost(self):
        pass
    #    if self.counsoler.level == 'GC':
    #        cost = self.GC_Cost * self.package.gcHours * ((self.gcEnd-self.gcStart)/(self.packEnd-self.packStart))
    #        return round(cost,2)  #enforce length type calculated with dateDiff
    #    elif self.counsoler.level == 'FAO':
    #        cost = self.FAO_Cost * self.package.faoHhours * ((self.gcEnd-self.gcStart)/(self.packEnd-self.packStart))
    #        return round(cost,2)
    
    def clean(self):
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
    
       
   # def __str__(self):
   #     return f'{self.students} has enrolled in {self.package}: {self.packStart} to {self.packEnd} with {self.counsolers}'
