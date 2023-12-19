from django import forms
from django.forms import widgets
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, DateInput
from portal.models import Event

class CreateUserForm(UserCreationForm):# to add email because the usercreation form doesn't have an email field
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField()

    class Meta:
        model=User
        fields=['username','email']      

class ProfileForm(forms.ModelForm):
   
    class Meta:
        model=Profile
        fields=['image']     

class NoteForm(forms.ModelForm):
    class Meta:
        model=Note
        fields=['title','description']

class DateInput(forms.DateInput):
    input_type ='date'        

class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished']        

  

class DashboardForm(forms.Form):
    text=forms.CharField(max_length=100, label='Enter your search') 
       

  
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']

class NotifytodoForm(forms.ModelForm):
    class Meta:
        model=Notifytodo
        fields=['title','status']
class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['text',]    
class BooksForm(forms.ModelForm):
    class Meta:
        model=Books
        fields=('bname', 'blist','is_finished')   

class TodocssForm(forms.ModelForm):
    class Meta:
        model=Todocss
        fields=['title','is_finished']          



class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
