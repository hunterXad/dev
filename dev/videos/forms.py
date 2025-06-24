from django import forms
from .models import Stream


class StreamForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['title', 'youtube_id', 'status','category']


class StreamStatusForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['status']