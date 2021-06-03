from django import forms


class SearchForm(forms.Form):
    title = forms.CharField( max_length=100, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))


class CreatePageForm(forms.Form):
    title = forms.CharField( max_length=50, label="", widget=forms.TextInput(
        attrs={ 'placeholder': 'Enter Title', 
                'style':'margin-bottom: 5px;',
        }))

    content = forms.CharField( label="", widget=forms.Textarea(
        attrs={ "style":"width: 500px; height: 250px;",
                'placeholder':'Enter Text', 
        }))


class EditPageForm(forms.Form):
    title = forms.CharField(max_length=50, label="", widget=forms.TextInput(
        attrs={ 'style':'margin-bottom: 5px;',}))

    content = forms.CharField( label="", widget=forms.Textarea(
        attrs={ "style":"width: 500px; height: 250px;" }))
    