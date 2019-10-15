from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import *

class TeacherSignUpForm(UserCreationForm):
    assign_class = forms.ModelMultipleChoiceField(queryset=ClassesName.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    subjects=forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        help_texts = {
            'username': None,
            'password1': None,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.assign_class.add(*self.cleaned_data.get('assign_class'))
        teacher.subjects.add(*self.cleaned_data.get('subjects'))
        return user


class StudentSignUpForm(UserCreationForm):
    def classChoice():
        queryset=ClassesName.objects.all()
        choicesdata=[]
        for data in queryset:
            choicesdata.append([data.id,data.name])
        return choicesdata

    Class =forms.ChoiceField(choices=classChoice(),
        widget=forms.Select,required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student1 = Student.objects.create(user=user,Class_id=self.cleaned_data.get('Class'))
        # student1.Class.add(*self.cleaned_data.get('Class'))
        return user
