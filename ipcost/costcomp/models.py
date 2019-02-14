from django.db import models
from datetime import date

#counsolers
class Counsoler(models.Model):
    COUNSOLER_LEVEL = (
        ('JR', 'Junior'),
        ('SR', 'Senior')
    )

    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    salary = models.IntegerField()
    guaranteed = models.IntegerField()
    level = models.CharField(max_length=3, choices=COUNSOLER_LEVEL, default='JR')

    @property
    def total(self): 
        return self.salary + self.guaranteed
    
    def __str__(self):
        return f'{self.firstName} {self.lastName} Total:{self.total} = Salary:{self.salary} + Guaranteed:{self.guaranteed}'


#packages
class Package(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    length = models.IntegerField()
    
    def __str__(self):
        return f'{self.name}: ${self.price} for {self.length} hours'


#students
class Student(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    counsolers = models.ManyToManyField(Counsoler, through='Enrollment') 
    def  __str__(self):
        return f'{self.firstName} {self.lastName}' 



#enrollment as intermediary
class Enrollment(models.Model):
    jrCounsCost = 50    #junior counsoler hourly cost
    srCounsCost = 100   #senior counsoler hourly cost

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollment')
    counsoler = models.ForeignKey(Counsoler, on_delete=models.CASCADE, related_name='enrollment')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='enrollment')
    startDate = models.DateField(default=date.today, blank=False)
    endDate = models.DateField(default=date.today, blank=False)
    
    @property
    def cost(self):
        if self.counsoler.level == 'JR':
            return self.jrCounsCost * self.package.length
        elif self.counsoler.level == 'SR':
            return self.srCounsCost * self.package.length
    
    def __str__(self):
        return f'{self.student} has enrolled in {self.package}: {self.startDate} to {self.endDate} with {self.counsoler.firstName}'
