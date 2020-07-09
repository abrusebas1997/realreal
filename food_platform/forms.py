from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from food_platform.models import (Answer, PickupTime, Foodriver, FoodriverAnswer,
                              Urgency, User)


class FoodonatorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_foodonator = True
        if commit:
            user.save()
        return user


class FoodriverSignUpForm(UserCreationForm):
    area = forms.ModelMultipleChoiceField(
        queryset=Urgency.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_foodriver = True
        user.save()
        foodriver = Foodriver.objects.create(user=user)
        foodriver.area.add(*self.cleaned_data.get('area'))
        return user


class FoodriverAreaForm(forms.ModelForm):
    class Meta:
        model = Foodriver
        fields = ('area', )
        widgets = {
            'area': forms.CheckboxSelectMultiple
        }


class PickupTimeForm(forms.ModelForm):
    class Meta:
        model = PickupTime
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakePickupForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = FoodriverAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        pickup_time = kwargs.pop('pickup_time')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = pickup_time.answers.order_by('text')
