# Generated by Django 5.0 on 2023-12-14 08:40

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(default=django.utils.timezone.now)),
                ('category', models.CharField(choices=[('Groceries', 'Groceries'), ('Fashion', 'Fashion'), ('Car', 'Car'), ('Bills', 'Bills'), ('Public Transport', 'Public Transport'), ('Property', 'Property'), ('Investing', 'Investing'), ('Healthcare', 'Healthcare'), ('Entertainment', 'Entertainment'), ('Education', 'Education'), ('Savings', 'Savings'), ('Travel', 'Travel')], max_length=25)),
                ('description', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-payment_date'],
            },
        ),
    ]
