from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #API urls
	url(r'^api/login/$', views.UserLoginView.as_view()),   # Login here 
    url(r'^api/notes/$', views.NoteCreateView.as_view()),  # List Create Notes
    url(r'^api/notes/(?P<note_id>[0-9a-f-]+)/$', views.UpdateDeleteNotesView.as_view()),
    url(r'^api/notes/(?P<note_id>[0-9a-f-]+)/label/$', views.LabelCreateView.as_view()),  # Label Create
    url(r'^api/notes/(?P<note_id>[0-9a-f-]+)/label/(?P<label_id>[0-9a-f-]+)/$', views.UpdateDeleteLableView.as_view()), 

    #WEBAPP url
    url(r'^$', auth_views.login, name='login'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^addnotes/$', login_required(views.AddNoteView),  name='createnotes'),
    url(r'^notes/$', views.NoteListView.as_view()),
    url(r'^notes/(?P<pk>[0-9a-f-]+)/$', views.NoteDetailView.as_view()),
    url(r'^notes/(?P<pk>[0-9a-f-]+)/update/$', views.UpdateNotesView.as_view()),
    url(r'^notes/(?P<note_id>[0-9a-f-]+)/remove/$',login_required(views.DeleteNotesView) , name='remove'),




   ] 