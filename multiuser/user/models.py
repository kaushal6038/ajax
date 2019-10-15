from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class ClassesName(models.Model):
	name = models.CharField(max_length=3)

	def __str__(self):
		return self.name

class Subjects(models.Model):
	name = models.CharField(max_length=12)

	def __str__(self):
		return self.name

class Student(models.Model):
	Class = models.ForeignKey(ClassesName,on_delete=models.CASCADE)
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

	def __str__(self):
		return self.user.username
    # quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    # interests = models.ManyToManyField(Subject, related_name='interested_students')

class Teacher(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	assign_class = models.ManyToManyField(ClassesName)
	subjects = models.ManyToManyField(Subjects)
	
	def __str__(self):
		return self.user.username