from django import forms
from Login.models import UserDetails, Question, Option, OptionHeader
from django.utils import timezone

class QuestionForm(forms.ModelForm):
    questionType=(
              ('1' , 'Subjective'),
              ('2' , 'MCQ'),
              ('1' , 'Scale')
         )
    intentType =(
                 ('1','+ve'),
                 ('2','-ve')
                )
    questionID=forms.CharField(required=False,widget=forms.HiddenInput(),initial='0')
    question = forms.CharField(error_messages={'required': 'Please enter question'}, widget=forms.Textarea(attrs={'rows':4,'class':'span4', 'style': 'width:auto;'}),label="Question")
    info = forms.CharField(error_messages={'required':'Enter question header'}, widget=forms.Textarea(attrs={'rows':2,'class':'span4', 'style': 'width:auto;'}), label="Question header")
    intent = forms.ChoiceField(choices=intentType, error_messages={'required': 'Please select intent'}, widget=forms.Select(attrs={'class':'tableRow span4 search-query', 'style': 'border-radius: 15px 15px 15px 15px;width:98%;'}),label="Intent")
    weight = forms.CharField(required=False,label="Question weight",initial=0)
    level = forms.CharField(required=False,label="Question level",initial=0)
    type = forms.ChoiceField(required=False,choices=questionType, error_messages={'required': 'Please select question type'},widget=forms.Select(attrs={'class':'tableRow span4 search-query', 'style': 'border-radius: 15px 15px 15px 15px;width:auto;'}),label="Question type")
    category=forms.CharField(required=False)
    type_text=forms.CharField(required=False,widget=forms.HiddenInput(),initial='Subjective')
    class Meta:
        model=Question
        fields=("questionID","question","level","weight","type","info","intent","type_text")
               
    def clean_level(self):
        if self.cleaned_data['level'] == '0':
            raise forms.ValidationError("Please select level of question.")
        return self.cleaned_data['level']
    
    def clean_weight(self):
        if self.cleaned_data['weight'] == '0':
            raise forms.ValidationError("Please select weight of question.")
        return self.cleaned_data['weight']
    
    
    def save(self,userId,optionHeaderId, commit=True):
        objQuestionForm = super(QuestionForm, self).save(commit=False)
        objQuestionForm.question = self.data['question']
        objQuestionForm.level = self.data['level']
        objQuestionForm.intent = self.data['intent']
        objQuestionForm.weight = self.data['weight']
        objQuestionForm.type = self.data['type_text']
        objQuestionForm.category = ''#self.data['category']
        if self.data['type_text'] == 'MCQ':
            objQuestionForm.option_header = optionHeaderId
        objQuestionForm.info = self.data['info']
        objQuestionForm.modified_by = userId
        objQuestionForm.modified_on = timezone.now()
        objQuestionForm.save() 


class OptionFrom(forms.ModelForm):
    option_header_text = forms.CharField(label="Option header",widget=forms.Textarea(attrs={'rows':2,'class':'span4', 'style': 'width:auto;'}),error_messages={'required':'Enter Option header'})
    option_text = forms.CharField(label="Options",widget=forms.HiddenInput(),error_messages={'required':'Enter Options'})
    option_header_id = forms.CharField(required=False,widget=forms.TextInput(attrs={'style':'display:none;'}),initial='0')
    
    class Meta:
        model=Option
        fields=("option_header_id","option_text","option_header_text")
    
#    def clean_optionheadertext(self, sOptionHeaderText, nOptionHeaderID):
#        error_msg=''
    
#        if nOptionHeaderID == '0':
#            objOptions = OptionHeader.objects.filter(title=sOptionHeaderText).count()
#            if objOptions> 0 :
#                raise forms.ValidationError("Option header already exists.")
#        return self.cleaned_data['option_header_text']
    
    def save(self, userId,optionHeaderId,commit=True ):
         objOptionFrom = super(OptionFrom, self).save(commit=False)
         options = (self.data['option_text']).split(",")
         for index, option in enumerate(options):
             arroption = option.split("|")
             objOptionFrom.option_header = optionHeaderId#OptionHeader.objects.latest('option_header_id')
             objOptionFrom.option_text = arroption[0]#self.data['option_text']
             objOptionFrom.option_level = arroption[1]
             objOptionFrom.order = index + 1
             objOptionFrom.modified_by = userId
             objOptionFrom.modified_on = timezone.now()
             objOptionFrom.save()
                 
         