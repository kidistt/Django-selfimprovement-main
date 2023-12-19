
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default='pexels.jpg',upload_to='profilepics')

    def __str__(self):
        return f'{self.user.username} Profile'
class Note(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=1000)

    def __str__(self):
        return self.title

class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    title=models.CharField(max_length=100)
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True, null=True)
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
       return self.subject





class Notifytodo(models.Model):
    Status=(
        ('finished','finished'),
        ('unfinished','unfinished'),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    status=models.CharField(max_length=10, choices=Status)

    def __str__(self):
        return self.title

class Diary(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    text=models.TextField()
    date=models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return 'Entry #{}'.format(self.id)    

class Books(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    bname=models.CharField(max_length=100)
    blist=models.FileField(upload_to='books')
    is_finished=models.BooleanField(default=False)


    def __str__(self):
        return self.bname
class Todocss(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    is_finished=models.BooleanField(default=False)
   
    def __str__(self):
       return self.title

class Quote(models.Model):
    quote=models.CharField(max_length=500)

    def __str__(self):
        return self.quote

class Event(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('eventedit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>' 
        
    def __str__(self):
        return self.title
      


    


