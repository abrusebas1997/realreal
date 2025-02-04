# Generated by Django 2.0.1 on 2018-01-18 18:07

from django.db import migrations


def create_interested_area(apps, schema_editor):
    Interested_area = apps.get_model('food_platform', 'Interested_area')
    Interested_area.objects.create(name='San Francisco', color='#8B008B')
    Interested_area.objects.create(name='Alameda', color='#B22222')
    Interested_area.objects.create(name='Tiburon', color='#8c79da')
    Interested_area.objects.create(name='Berkeley', color='#FF4500')
    Interested_area.objects.create(name='Oakland', color='#d279da')
    Interested_area.objects.create(name='Emeryville', color='#687f6a')
    Interested_area.objects.create(name='Daly City', color='#343a40')
    Interested_area.objects.create(name='San Jose', color='#af7f6a')



class Migration(migrations.Migration):

    dependencies = [
        ('food_platform', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_interested_area),
    ]
