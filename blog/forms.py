from django import forms


from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50, label="Ник")
    email = forms.EmailField()
    recipient = forms.EmailField(label="Кому")
    comment = forms.CharField(required=False, widget=forms.Textarea, label="Сообщение")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "content"]
        labels = {
            "name": "Ник",
            "content": "Комментарий"
        }


class SearchForm(forms.Form):
    query = forms.CharField(label="Запрос")