from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Sum, Avg, Case, When, F
from django.core.paginator import Paginator

import plotly.express as px
import plotly.graph_objects as go

from .models import Payment
from .forms import DateForm
from .helper_functions import months_labels_func


# Create your views here.

def home_view(request):

    current_user = request.user
    context = {'user': current_user}

    if current_user.is_authenticated:
        payments = Payment.objects.filter(user=current_user)
        context['payments'] = payments
        debit = payments.filter(payment_type='Debit')
        if payments:
            monthly_chart = monthly_chart_func(debit)
            pie_chart = pie_chart_func(debit)
            savings_chart, avg_savings = monthly_savings_chart_func(payments)
            context['savings_chart'] = savings_chart
            context['avg_savings'] = f'{avg_savings:.2f}'

            context['m_chart'] = monthly_chart
            context['pie_chart'] = pie_chart

            avg_spending = debit.filter(payment_type='Debit').values('payment_date__month').annotate(
                m_sum=Sum('amount')).aggregate(Avg('m_sum'))
            context['avg_spending'] = f"{avg_spending['m_sum__avg']:.2f}"

            p = Paginator(payments, per_page=20)
            page = request.GET.get('page')
            payments_page = p.get_page(page)
            context['payments_page'] = payments_page

    return render(request, 'main/home.html', context=context)


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    _url = reverse_lazy('login')


class CreatePayment(CreateView):
    model = Payment
    fields = ['payment_date', 'category', 'description', 'payment_type','amount']
    template_name = 'main/create_payment.html'
    success_url = reverse_lazy('home view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditPaymentView(UpdateView):
    model = Payment
    template_name = 'main/edit_payment.html'
    fields = ['payment_date', 'category', 'description', 'payment_type','amount']
    success_url = reverse_lazy('home view')


class DeletePaymentView(DeleteView):
    model = Payment
    template_name = 'main/delete_payment.html'
    success_url = reverse_lazy('home view')


def index(request):

    return redirect('home view')


def logout_view(request):
    logout(request)
    # messages.success(request, message='You have successfully logged out.') 
    return redirect('home view')


def monthly_chart_func(dataset):
    months_dict = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    x_y_data = dataset.values('payment_date__month').annotate(per_month=Sum('amount'))
    x_axis = []
    y_axis = []
    for item in x_y_data:
        x_axis.append(months_dict[item['payment_date__month']])
        y_axis.append(item['per_month'])

    fig = px.bar(
        x=x_axis,
        y=y_axis,
        title='Spending Summary',
        text_auto='.2s'
    )
    fig.update_layout(yaxis_title=None, xaxis_title=None)
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
    payments = Payment.objects.filter(user=request.user, payment_type='Debit')
    form = DateForm()
    context = {'form': form}

    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    categories = request.GET.getlist('categories')
    search_data = {'start': start, 'end': end, 'categories': categories}

    if start:
        payments = payments.filter(payment_date__gte=start)
    if end:
        payments = payments.filter(payment_date__lte=end)
    if categories:
        payments = payments.filter(category__in=categories)
        categories_list = ', '.join(categories)
        search_data['categories_list'] = categories_list
    
    stacked_chart = stacked_bar(payments, categories)
    context['stacked_chart'] = stacked_chart
    context['search_data'] = search_data

    return render(request, 'main/custom_chart.html', context)


def monthly_savings_chart_func(dataset):
    
    months_dict = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    x_data = []
    y_data = []
    savings = dataset.values('payment_date__month').annotate(
        balance=Sum(Case(When(payment_type='Credit', then=F('amount')), default=-F('amount')))
    )
    for item in savings:
        x_data.append(months_dict[item['payment_date__month']])
        y_data.append(item['balance'])
    
    fig = px.bar(
        x=x_data,
        y=y_data,
        title='Savings Summary',
        text_auto='.0f',
        color_discrete_sequence=['seagreen']  
    )
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    average_savings = sum(y_data) / len(y_data)
    return fig.to_html(), average_savings


def contacts(request):
    return render(request, 'main/contacts.html')


def stacked_bar(dataset, categories):

    dataset = dataset.values('payment_date__month', 'category').annotate(sum_per_cat=Sum('amount'))
    all_charts = []

    for cat in categories:
        current_y_axis = dataset.filter(category=cat)
        months_queryset = current_y_axis.values_list('payment_date__month', flat=True)
        months_labels = months_labels_func(months_queryset)
 
        current_y_axis = dataset.filter(category=cat).values_list('sum_per_cat', flat=True)
        y_axis = [f'{item:.2f}' for item in current_y_axis]
        current_bar = go.Bar(name=cat, x=months_labels, y=list(current_y_axis), text=y_axis)
        all_charts.append(current_bar)  

    fig = go.Figure(data=[*all_charts])
    fig.update_layout(barmode='stack')
    fig.update_xaxes(
        categoryorder='array',
        categoryarray= ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    chart = fig.to_html()
    
    return chart


def account_details(request):
    if request.user.is_authenticated:
        context = {'user': request.user}
        return render(request, 'registration/account_details.html', context)

    return redirect('home view')
