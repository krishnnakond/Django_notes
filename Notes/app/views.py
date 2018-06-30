# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout		
from .models import Notes, User, Label
from .forms import NoteForm
from django.http import HttpResponseRedirect
from .serializers import UserLoginSerializer, NotesSerializer, LabelSerializer
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        #print(request.data)
        try:
            if 'username' in request.data and 'password' in request.data:
                user = authenticate(username=request.data['username'], password=request.data['password'])
                if user is not None:
                    login(request, user)
                    serializer = UserSerializer(user)
                    return Response({"success": True, "msg": "You are logged-in successfully"})
                else:
                    return Response({"success": False, "msg": "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"success": False, "msg": "Username & password is required"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e) 
            return Response({"success": False, "msg": "something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)



class NoteCreateView(generics.ListCreateAPIView):
    serializer_class = NotesSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Notes.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


    def filter_queryset(self, queryset):
        return queryset.filter(user =self.request.user)


class UpdateDeleteNotesView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = NotesSerializer
	authentication_classes = (SessionAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def get_object(self):
		return get_object_or_404(Notes, pk=self.kwargs['note_id'])


class LabelCreateView(generics.ListCreateAPIView):
    serializer_class = LabelSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Label.objects.all()

    def get_serializer_context(self):
        return {'request': self.request, "note":self.kwargs['note_id']}


class UpdateDeleteLableView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = LabelSerializer
	authentication_classes = (SessionAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def get_object(self):
		return get_object_or_404(Label, pk=self.kwargs['label_id'])

 


 

class NoteListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'my_note'  
    queryset = Notes.objects.all()  
    template_name = 'listnotes.html'  

    def get_queryset(self):
        return Notes.objects.filter(user=self.request.user)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    slug_field = 'note_id'
    context_object_name = 'my_note'
    template_name = 'detailnotes.html'  



def AddNoteView(request):
    user = request.user
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
        	new_note = form.save(commit=False)
        	new_note.user = request.user
        	new_note.save()
        	return HttpResponseRedirect('/notes/')
    return render(request, 'notepage.html', {'form': NoteForm()})
    

def DeleteNotesView(request, **kwargs):
	note = kwargs['note_id'] 
	Notes.objects.get(id=note, user=request.user).delete()
	return HttpResponseRedirect('/notes/')
	

class UpdateNotesView(LoginRequiredMixin, UpdateView):
    model = Notes
    fields = ['note']
    context_object_name = 'my_note'
    template_name = "updatenotes.html"
    success_url="/notes/"