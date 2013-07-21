from django import forms
from Login.models import UserDetails, Question

class QuestionForm(forms.ModelForm):
    questionType=(
              ('select' , '--SELECT--'),
              ('MCQ' , 'MCQ'),
              ('Subjective' , 'Subjective')
         )
    objquestion = forms.CharField(error_messages={'required': 'Please enter question'}, widget=forms.Textarea(attrs={'rows':4}),label="Question")
    objinfo = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), label="Additional information (optional)")
    objintent = forms.CharField(error_messages={'required': 'Please select intent'}, widget=forms.TextInput(attrs={'class':'tableRow span4 search-query'}),label="Intent")
    objlevel = forms.CharField(label="Question level")
    objweight = forms.CharField(label="Question weight")
    objtype = forms.ChoiceField(choices=questionType, error_messages={'required': 'Please select question type'},widget=forms.Select(attrs={'class':'tableRow span4 search-query', 'style': 'border-radius: 15px 15px 15px 15px;'}),label="Question type")
        
    class Meta:
        model=Question
        fields=("objquestion","objlevel","objweight","objtype","objinfo","objintent")
    