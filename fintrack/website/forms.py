from django import forms


class DateForm(forms.Form):
    
    CATEGORY_CHOICES = {
        'All': 'All',
        'Groceries': 'Groceries',
        'Fashion': 'Fashion',
        'Car': 'Car',
        'Bills': 'Bills',
        'Public ransport': 'Public Transport',
        'Property': 'Property',
        'Investing': 'Investing',
        'Healthcare': 'Healthcare',
        'Entertainment': 'Entertainment',
        'Education': 'Education',
        'Savings': 'Savings',
        'Travel': 'Travel'
    }
        
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES, required=False)
