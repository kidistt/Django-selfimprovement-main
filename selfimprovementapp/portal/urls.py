from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.homeone,name='homeone'),
    path('home',views.home, name='home'),
   
    path('register',views.registration, name='register'),
    path('login',views.loginpage,name='login'),
    path('notes',views.notes, name='notes'),
    path('delete-notes/<int:pk>/',views.delete_notes,name='delete-note'),
    path('notesdetail/<int:pk>',views.notesdetail, name='notesdetail'),
    path('notesedit<int:pk>',views.editnotes, name='editnotes'),
    path('createnote',views.createnote,name='createnote'),
    path('homework',views.homework, name='homework'),
    path('homeworkform',views.homeworkform, name='homeworkform'),
    path('edithomework/<int:pk>',views.edithomework, name='edithomework'),
    path('update_homework/<int:pk>',views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>/', views.delete_homework, name='delete-homework'),
    path('book',views.books,name='book'),
    path('bookdelete/<int:pk>/',views.booksdelete,name='bookdelete'),
    path('bookupdate/<int:pk>/',views.book_update,name='bookupdate'),
    path('bookform',views.book_form,name='bookform'),
    
    path('wiki',views.wiki, name='wiki'),
    path('timer',views.timer, name='timer'),
    path('notify',views.notifytodo, name='notify'),
    path('notifydelete<int:pk>',views.notifydelete,name='notifydelete'),
    path('edittodo<int:pk>',views.edit_todo,name='edittodo'),
    # path('popup', views.popup, name='popup'),
    path('diary',views.diary,name='diary'),
    path('diaryedit/<int:pk>/',views.diaryedit,name='diaryedit'),
    path('deletediary/<int:pk>/',views.deletediary,name='deletediary'),
    path('adddiary',views.adddiary, name='adddiary'),
    path('emotion',views.emotion, name='emotion'),
    path('tocss',views.tocss,name='tocss'),
    path('calorie',views.calorie, name='calorie'),
    path('calendar/',views.CalendarView.as_view(), name='calendar'),
    path('event',views.event,name='event'),
    path('eventedit<int:pk>',views.event,name='eventedit'),
    path('eventdelete<int:pk>',views.delete_event,name='eventdelete'),
    path('profile',views.profile, name='profile'),
    path('animated',views.animated,name='animated'),
    
  
    path('activate/<uidb64>/<token>', views.activate, name='activate')
    
    
    
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)