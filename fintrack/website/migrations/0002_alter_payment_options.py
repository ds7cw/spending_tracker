# Generated by Django 5.0 on 2023-12-14 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['user__id', '-payment_date']},
        ),
    ]
