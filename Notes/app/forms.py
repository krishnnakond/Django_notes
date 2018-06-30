

from django.forms import ModelForm
from .models import Notes, Label









class NoteForm(ModelForm):
    class Meta:
        model = Notes
        fields = ('note',)