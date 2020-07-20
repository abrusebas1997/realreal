from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_foodriver = models.BooleanField(default=False)
    is_foodonator = models.BooleanField(default=False)

# change for interested_area
class Interested_area(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Pickup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickups')
    name = models.CharField(max_length=255)
    interested_area = models.ForeignKey(Interested_area, on_delete=models.CASCADE, related_name='pickups')

    def __str__(self):
        return self.name


class PickupTime(models.Model):
    pickup = models.ForeignKey(Pickup, on_delete=models.CASCADE, related_name='pickup_times')
    text = models.CharField('PickupTime', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    pickup_time = models.ForeignKey(PickupTime, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Foodriver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pickups = models.ManyToManyField(Pickup, through='TakenPickup')
    area = models.ManyToManyField(Interested_area, related_name='interested_foodrivers')

    def get_unanswered_pickup_times(self, pickup):
        answered_pickup_times = self.pickup_answers \
            .filter(answer__pickup_time__pickup=pickup) \
            .values_list('answer__pickup_time__pk', flat=True)
        pickup_times = pickup.pickup_times.exclude(pk__in=answered_pickup_times).order_by('text')
        return pickup_times

    def __str__(self):
        return self.user.username


class TakenPickup(models.Model):
    foodriver = models.ForeignKey(Foodriver, on_delete=models.CASCADE, related_name='taken_pickups')
    pickup = models.ForeignKey(Pickup, on_delete=models.CASCADE, related_name='taken_pickups')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class FoodriverAnswer(models.Model):
    foodriver = models.ForeignKey(Foodriver, on_delete=models.CASCADE, related_name='pickup_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
