from datetime import datetime,timedelta, date,timezone
from operator import truediv
from pickle import FALSE, TRUE
import time
import email
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from . forms import *
from .forms import EventForm
import calendar
from . models import *
from .utils import Calendar



import wikipedia
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login 

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token



# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user =User.objects.get(pk=uidb64)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
         user.is_active =True
         user.save()

         messages.success(request, "thank you for your email confirmation. Now you can login in your account.")
         return redirect('login')
    else:
        messages.error(request, "Activation is invalid!")

    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_actiavte_account.html", 
    {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol":'https'if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject,message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user}, please go to your email {to_email} inbox and click on the received activation link to confirm and commplete the registartion. ")
    else:
        messages.error(request, f'problem sending email to {to_email}, check if you typed it correctly')

        
def homeone(request):
    return render(request,'homeone.html')
@login_required
def home(request):
    
    todonotify=Notifytodo.objects.filter(user=request.user,status = 'unfinished')
    
    context={'todonotify':todonotify}
    
    

    return render(request,'home.html',context) 

def registration(request):
       
       
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
               user = form.save(commit=False)
               user.is_active=False
               user.save()

               activateEmail(request, user, form.cleaned_data.get('email'))
               return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
         form = CreateUserForm()
      
        return render(request,'register.html',context={"form":form}) 

def loginpage(request):
    if request.method=='POST':
         username=request.POST.get('username')
         password=request.POST.get('password')
         user=authenticate(request, username=username, password=password)
         if user is not None:
            login(request, user)
            return redirect('home')
    
         messages.info(request,'Username Or password is incorrect')    
         
    return render(request,'login.html')   


                  
@login_required
def notes(request):
    notes=Note.objects.filter(user=request.user)
    context={'notes':notes}
    return render(request,'notes.html',context)      
@login_required
def createnote(request):
    if request.method == 'POST':
        form=NoteForm(request.POST)
        if form.is_valid():
            note=Note(user=request.user,title=request.POST['title'],description=request.POST['description'])
            note.save()

            return redirect('notes')
    else:
        form=NoteForm
    
    context={'form':form,'notes':notes}    
    return render(request,'noteform.html',context)        

@login_required
def delete_notes(request,pk=None):
    Note.objects.get(id=pk).delete()
    return redirect('notes')
@login_required
def notesdetail(request,pk):
    notes=Note.objects.get(id=pk)
    return render(request,'notes-detail.html',{'notes':notes})
@login_required
def editnotes(request,pk):
    notes=Note.objects.get(id=pk)
    form=NoteForm(request.POST or None, instance=notes)
    if form.is_valid():
        form.save()
        return redirect('notes')

    return render(request,'noteedit.html',{'form':form})
    


@login_required
def homework(request):
    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False  
     
    context={'homework':homework, 'homework_done':homework_done}
    return render(request,'homework.html', context)
@login_required
def homeworkform(request):
    if request.method=='POST':
        form=HomeworkForm(request.POST)
        
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    finished =False
            except:
                finished=False        
                homeworks =Homework(
                    user=request.user,
                    subject=request.POST['subject'],
                    title=request.POST['title'],
                    description=request.POST['description'],
                    due=request.POST['due'],
                    is_finished=finished,
                )  
                homeworks.save()   
                
                messages.success(request,f'homework added from {request.user.username}!!') 
                return redirect('homework')  
    else:        
        form=HomeworkForm()

           
    context={'homework':homework,'form':form}
    return render(request,'homeworkform.html', context)

@login_required
def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished=False
    else:
        homework.is_finished=True   
    homework.save()
    return redirect('homework') 
@login_required       
def edithomework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    form=HomeworkForm(request.POST or None, instance=homework)
    if form.is_valid():
        form.save()
        return redirect('homework')
    
    return render(request,'edithomework.html',{'form':form})
@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')




#notifications



    
     

@login_required    
def wiki(request):
    if request.method == 'POST':
        text =request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary

        }
        return render(request,'wiki.html', context)
    else:
        form=DashboardForm()
        context={
            'form':form
        }    
    return render(request,'wiki.html',context)



def timer(request):
    return render(request,'timer.html')

def notifytodo(request):
    if request.method =='POST':
        form=NotifytodoForm(request.POST)
        if form.is_valid():
            notify=Notifytodo(user=request.user, title=request.POST['title'], status=request.POST['status'])
            notify.save()

    else:
        form=NotifytodoForm
    notify=Notifytodo.objects.filter(user=request.user)   
    todonotify=Notifytodo.objects.filter(user=request.user,status = 'unfinished')
    context={'notify':notify, 'form':form,'todonotify':todonotify}         

    return render(request,'todonotify.html', context)   

def notifydelete(request,pk=None):
    Notifytodo.objects.get(id=pk).delete() 
    return redirect('notify')    

def edit_todo(request,pk=None):
    notify=Notifytodo.objects.get(id=pk)
    form=NotifytodoForm(request.POST or None, instance=notify)
    if form.is_valid():
        form.save()
        return redirect('notify')

    return render(request,'edittodo.html',{'form':form})


# def popup(request):
#     notify=Notifytodo.objects.filter(user=request.user)   
#     todonotify=Notifytodo.objects.filter( status = 'unfinished')
#     context={'notify':notify,'todonotify':todonotify}   
#     return render(request,'popup.html',context)    
def diary(request):
    diary=Diary.objects.order_by('date')
    context={'diary':diary}
    return render(request,'diary.html',context)

def adddiary(request):
    if request.method == "POST":
        form=DiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary')

    else:
        form=DiaryForm()     
    context = {'form' : form}      
   
    return render(request,'adddiary.html',context)

  

def books(request):
    books=Books.objects.filter(user=request.user)    
    context={'books':books}     
    return render(request,'books.html',context) 

def book_form(request):
    if request.method =='POST':
        form=BooksForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                finished=request.POST['is_finihsed']
                if finished == 'on':
                    finished=True
                else:
                    finished = False
            except:
                finished = False    

                          
            book =Books(user=request.user, bname=request.POST['bname'], blist=request.FILES['blist'],is_finished=finished)
            book.save()
            return redirect('book')  

    else:
        form=BooksForm()
    context={'books':books,'form':form}
    return render(request,'bookform.html',context)


def booksdelete(request,pk=None):
    Books.objects.get(id=pk).delete() 
    return redirect('book')   

def book_update(request,pk=None):
    books=Books.objects.get(id=pk)
    if books.is_finished == True:
        books.is_finished = False

    else:
        books.is_finished = True

    books.save()
    return redirect('book')  
    






def emotion(request):
    return render(request,'emotion.html')

def calorie(request):
    import json
    import requests

    if request.method == 'POST':
        query =request.POST['query']
        api_url= 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request= requests.get(api_url + query, headers={'X-Api-Key': 'DNFsg/3Jn0s48Rrt29Am4g==v0NRz1P0BTjY40lq'})
        try:
            api= json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api= "oops! there was an error"    
            print(e)
        return render(request,'calorie.html',{'api':api})    
    else:
        return render(request,'calorie.html',{'query':'enter a valid query'})   

def tocss(request):
    if request.method == 'POST':
        form=TodocssForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False 
            except:
                finished=False
            todocss=Todocss(user=request.user,title=request.POST['title'],is_finished=finished)
            todocss.save()

    else:
        form=TodocssForm

        todocss=Todocss.objects.filter(user=request.user)
        context={'form':form,'todocss':todocss}        


    return render(request,'tocss.html',context)   

class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        portal = Calendar(d.year, d.month)
        html_cal = portal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, pk=None):
    instance = Event()
    if pk:
        instance = get_object_or_404(Event, pk=pk)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'event.html', {'form': form})  

def delete_event(request,pk):
    Event.objects.get(id=pk).delete()
    return redirect('calendar')     



    
    return render(request, 'myevents.html',{'notifycalendar':notifycalendar})     

def diaryedit(request, pk=None):
    diary=Diary.objects.get(id=pk)
    form=DiaryForm(request.POST or None, instance=diary)
    if form.is_valid():
        form.save()
        return redirect('diary')
    return render(request,'diaryedit.html',{'form':form})

def deletediary(request, pk=None):
    Diary.objects.get(id=pk).delete()
    return redirect('diary')    

def profile(request):
    if request.method == 'POST': 
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

       




            
    todonotify=Notifytodo.objects.filter(user=request.user,status = 'unfinished')
    tonotify=Notifytodo.objects.filter(user=request.user,status= 'finished')
    booknotify=Books.objects.filter(user=request.user,is_finished = True)
    
     
    notifycalendar=Event.objects.filter()
    context ={
        'u_form':u_form,
        'p_form':p_form,
        'todonotify':todonotify,
        'tonotify':tonotify,
        'notifycalendar':notifycalendar,
        'booknotify':booknotify,
        
        
    }
   
    return render(request, 'profile.html',context)
def animated(request):
    return render(request,'animated.html')



