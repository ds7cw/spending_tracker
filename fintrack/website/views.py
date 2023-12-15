from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
import plotly.express as px

from .models import Payment

# Create your views here.

def demo_view(request):
    current_user = request.user
    payments = Payment.objects.filter(user=current_user)
    context = {'payments': payments, 'user': current_user}

    return render(request, 'main/demo.html', context=context)


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    _url = reverse_lazy('login')


class CreatePayment(CreateView):
    model = Payment
    fields = ['payment_date', 'category', 'description', 'amount']
    template_name = 'main/create_payment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def index(request):
    x_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    y_list = [20.25, 12.75, 6.50, 4.99, 10.20, 45, 6]

    y_labels = [f'£{x}' for x in y_list]

    fig = px.bar(
        x=x_list,
        y=y_list,
        title='Weekly Expenses Summary',
        labels={'x': 'Day of the Week', 'y': 'Amount'},
        text=y_labels,
    )

    fig.update_layout(
        title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5
        },
        yaxis_range=[0,1.1 * max(y_list)],
    )

    chart = fig.to_html()
    context = {'chart': chart}
    return render(request, 'main/index.html', context)