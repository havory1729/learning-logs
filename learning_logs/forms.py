from django import forms

from .models import Entries, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text"]
        labels = {"text": ""}


class EntriesForm(forms.ModelForm):
    class Meta:
        model = Entries
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}
