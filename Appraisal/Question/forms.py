from django import forms
from Login.models import Question
class QuestionForm(forms.ModelForm):
 
    class Meta:
        model=Question
        fields=("question","level","weight","type","info","intent")
    