from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Payment(models.Model):
    """
        user: ForeignKey
        payment_date: DateField
        category: Groceries, Fashion, Car, Bills, Public Transport, Property, Investing, Healthcare, Entertainment, Education, Savings, Travel
        description: CharField(max_length=50)
        amount: DecimalField
    """

    CATEGORY_CHOICES = (
        ('Groceries', 'Groceries'),
        ('Fashion', 'Fashion'),
        ('Car', 'Car'),
        ('Bills', 'Bills'),
        ('Public Transport', 'Public Transport'),
        ('Property', 'Property'),
        ('Investing', 'Investing'),
        ('Healthcare', 'Healthcare'),
        ('Entertainment', 'Entertainment'),
        ('Education', 'Education'),
        ('Savings', 'Savings'),
        ('Travel', 'Travel')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])


    class Meta:
        ordering = ['user__id' ,'-payment_date']

    def __str__(self) -> str:
        return f'{self.payment_date} - {self.category} - £{self.amount}'

    def get_absolute_url(self):
        return reverse('demo view')