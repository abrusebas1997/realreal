from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from food_platform.models import (Answer, PickupTime, Foodriver, FoodriverAnswer,
                              Interested_area, User)


class FoodonatorSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_foodonator = True
        if commit:
            user.save()
        return user


class FoodriverSignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    area = forms.ModelMultipleChoiceField(
        queryset=Interested_area.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Don't worry, you can always change your preferred area"

    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'area')

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
