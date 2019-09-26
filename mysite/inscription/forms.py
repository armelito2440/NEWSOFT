from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "Nom d'utilisateur")
    password = forms.CharField(label = "Mot de passe",widget = forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 50,label = "Nom d'utilisateur")
    password = forms.CharField(max_length=20,label = "Mot de passe",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label ="Confirmer le mot de passe",widget = forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")

        values = {
            "username" : username,
            "password" : password
        }
        return values


