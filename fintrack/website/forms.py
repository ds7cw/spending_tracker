from django import forms


class DateForm(forms.Form):
    
    CATEGORY_CHOICES = {
        'Bills': 'Bills',
        'Car': 'Car',
        'Education': 'Education',
        'Entertainment': 'Entertainment',
        'Fashion': 'Fashion',
        'Groceries': 'Groceries',
        'Healthcare': 'Healthcare',
        'Investing': 'Investing',
        'Property': 'Property',
        'Public Transport': 'Public Transport',
        'Savings': 'Savings',
        'Travel': 'Travel'
    }
        
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES, required=False)
