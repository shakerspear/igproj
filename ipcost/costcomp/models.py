from django.db import models

#counsolers
class Counsoler(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    salary = models.IntegerField()
    guaranteed = models.IntegerField()
    
    @property
    def total(self): 
        return self.salary + self.guaranteed
    
    def __str__(self):
        return f'{self.id} - {self.firstName} {self.lastName} Total:{self.total} = Salary:{self.salary} + Guaranteed:{self.guaranteed}'


#packages
class Package(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}: ${self.price}'


#students
class Student(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='students')
    counsolers = models.ManyToManyField(Counsoler, blank=True, related_name='students')
#    startMonth = models.DateTimeField(default=datetime.now, blank=false)
#    endMonth = models.DateTimeField(default=self.startMonth

    def  __str__(self):
       return f'{self.firstName} {self.lastName}' 
