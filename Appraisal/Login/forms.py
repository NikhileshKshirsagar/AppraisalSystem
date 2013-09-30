from django import forms
from models import UserDetails        

class LoginForm(forms.ModelForm):
    txtUserName = forms.CharField(
                                  label='User Name',
                                  required=True,
                                  widget=forms.TextInput(attrs={'placeholder':'User Name'}),
                                  error_messages={'required':'Enter user name'}
                                  )#forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))
    
    txtPassword = forms.CharField(
                                  label='Password',
                                  required=True,
                                  widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
                                  error_messages={'required':'Enter password'}
                                  )#forms.DateField(widget=forms.TextInput(attrs={'class':'vDateField'}))   
    class Meta:
        model=UserDetails
        fields=("txtUserName","txtPassword")
    
    def Authenticate(self):
        iUserID =0
        try:
            objUserID = UserDetails.objects.filter(username__iexact=(self.data['txtUserName']).lower()).filter(password=self.data['txtPassword'])
            for u in objUserID:
                iUserID = u.user_id 
        except UserDetails.DoesNotExist:
            iUserID =0
        
        return iUserID
    
    