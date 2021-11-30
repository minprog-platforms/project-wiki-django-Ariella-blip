from django import forms

class CreatePageForm(forms.Form):
    entry_title = forms.CharField()
    entry_body = forms.CharField(widget = forms.Textarea)