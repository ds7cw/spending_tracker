from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator

import plotly.express as px
import plotly.graph_objects as go

from .models import Payment
from .forms import DateForm


# Create your views here.

def demo_view(request):

    current_user = request.user
    context = {'user': current_user}

    if current_user.is_authenticated:
        payments = Payment.objects.filter(user=current_user)
        context['payments'] = payments
        if payments:
            monthly_chart = monthly_chart_func(payments)
            pie_chart = pie_chart_func(payments)
            context['m_chart'] = monthly_chart
            context['pie_chart'] = pie_chart

            p = Paginator(payments, per_page=20)
            page = request.GET.get('page')
            payments_page = p.get_page(page)
            context['payments_page'] = payments_page

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


def logout_view(request):
    logout(request)
    # messages.success(request, message='You have successfully logged out.') 
    return redirect('demo view')


def monthly_chart_func(dataset):
    months = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    x_y_data = dataset.values('payment_date__month').annotate(per_month=Sum('amount'))
    x_axis = []
    y_axis = []
    for item in x_y_data:
        x_axis.append(months[item['payment_date__month']])
        y_axis.append(item['per_month'])

    fig = px.bar(
        x=x_axis,
        y=y_axis,
        title='Monthly Spending Summary',
    )
    return fig.to_html()


def pie_chart_func(dataset):
    x_y_data = dataset.values('category').annotate(category_sum=Sum('amount'))
    x_axis = []
    y_axis = []
    for item in x_y_data:
        x_axis.append(item['category'])
        y_axis.append(item['category_sum'])
    
    fig = go.Figure(data=[go.Pie(labels=x_axis, values=y_axis, hole=.3)])
    return fig.to_html()
    

def custom_chart(request):
    payments = Payment.objects.filter(user=request.user)
    form = DateForm()
    context = {'form': form}

    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    category = request.GET.getlist('category')
    search_data = {'start': start, 'end': end, 'category': category}

    if start:
        payments = Payment.objects.filter(payment_date__gte=start)
    if end:
        payments = payments.filter(payment_date__lte=end)
    if category:
        payments = payments.filter(category__in=category)
        category_list = ', '.join(category)
        search_data['category_list'] = category_list
        
    monthly_chart = monthly_chart_func(payments)
    context['monthly_chart'] = monthly_chart
    context['search_data'] = search_data

    return render(request, 'main/custom_chart.html', context)


def contacts(request):
    return render(request, 'main/contacts.html')