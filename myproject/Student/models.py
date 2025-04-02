from django.db import models

class Studentdetails(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=3)
    department = models.CharField(max_length=5)
    
    def __str__(self):
        return self.name

class Studentmarks(models.Model):
    student = models.OneToOneField(Studentdetails, on_delete=models.CASCADE, related_name='testmarks')
    subject1 = models.IntegerField()
    subject2 = models.IntegerField()
    subject3 = models.IntegerField()
    subject4 = models.IntegerField()
    subject5 = models.IntegerField()
    
    def __str__(self):
        return f"{self.student} - marks = {self.subject1},{self.subject2},{self.subject3},{self.subject4},{self.subject5}"
