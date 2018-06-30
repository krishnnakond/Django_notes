from rest_framework import serializers
from .models import Notes, User, Label
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist



class NotesSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Notes
        fields = ('id', 'note', 'user','created','updated')
        read_only_fields = ('id','user','created','updated')

    def create(self, validated_data):
        try:
            user = User.objects.get(id=self.context['request'].user.id)
        except ObjectDoesNotExist:
        	raise validationerror({'Error': "Permission Denied"})
        note = Notes.objects.create(**validated_data)
        note.user = user
        note.save()
        return note




class LabelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Label
		fields = ('id','name','created','updated')
		read_only_fields = ('id', 'note','created','updated')

	def create(self, validated_data):
		try:
			user = User.objects.get(id = self.context['request'].user.id)
			note = Notes.objects.get(id = self.context['note'], user = user)
		except ObjectDoesNotExist:
			raise ValidationError({"Error": "Permission Denied"})
		label = Label.objects.create(**validated_data)
		label.notes = note
		label.save()
		return label



class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    username = serializers.EmailField(allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'password')


