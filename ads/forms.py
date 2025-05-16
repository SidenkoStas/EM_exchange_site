from django import forms
from .models import Ad, ExchangeProposal

class CreateAdForm(forms.ModelForm):
    """
    Форма для создания объявления.
    """
    class Meta:
        model = Ad
        fields = ("category", "title", "description", "condition")

class ExchangeForm(forms.ModelForm):
    """
    Форма для запроса обмена.
    С фильтрациец товаров отправителя по пользователю.
    """
    class Meta:
        model = ExchangeProposal
        fields = ("ad_sender", "comment", "status")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["ad_sender"].queryset = Ad.objects.filter(user=user)