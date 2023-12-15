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

print(emmas_payments)
# print(emmas_payments.first().payment_date.month)

december_payments = emmas_payments.filter(payment_date__month=12)
print(december_payments)

november_payments = emmas_payments.filter(payment_date__month=11)
print(november_payments)