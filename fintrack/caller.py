import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fintrack.settings")
django.setup()


from django.contrib.auth.models import User
from website.models import Payment



# user_2 = User.objects.get(id=2)
# payments = Payment.objects.first()
# print(payments.user)

# Payment.objects.create(
#     user=user_2,
#     category='Education',
#     description='Udemy',
#     amount=15.99,
#     payment_date='2023-12-02'
# )

emma_user = User.objects.get(email='emma@emma.com')

# Payment.objects.create(
#     payment_date='2023-11-29',
#     category='Investing',
#     description='Stocks',
#     amount=100,
#     user=emma_user,
# )

emmas_payments = Payment.objects.filter(user=emma_user)

# print(emmas_payments)
# print(emmas_payments.first().payment_date.month)

# december_payments = emmas_payments.filter(payment_date__month=12)
# print(december_payments)

# november_payments = emmas_payments.filter(payment_date__month=11)
# print(november_payments)
# import random

# my_range=range(90, 210)
# my_date_range=range(18, 26)
# alex_user = User.objects.get(id=2)
# for i in range(1, 13):
    # my_day = random.choice(my_date_range)
    # my_date=f'2023-{i}-28'
    # my_amount=random.choice(my_range)
    # print(my_date)
    # print(my_amount)
    # Payment.objects.create(
    #     user=alex_user,
    #     payment_date=my_date,
    #     category='Savings',
    #     description='Savings Account',
    #     amount=my_amount
    # )

alex_payments = Payment.objects.select_related('user').filter(user__id=2)
# print(alex_payments)
from django.db.models import Sum

categories = ['Savings', 'Investing']

after_filter = alex_payments.filter(payment_date__lte='2023-03-31', category__in=categories)
# print(filtered)
after_values = after_filter.values('payment_date__month', 'category').annotate(sum_per_cat=Sum('amount'))
print(after_values)

master_container = {}

for cat in categories:
    print(after_values.filter(category=cat).values_list('sum_per_cat', flat=True))
    # master_container[cat] = after_values.values('sum_per_')