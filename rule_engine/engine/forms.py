from django import forms

class RuleForm(forms.Form):
    rule_string = forms.CharField(widget=forms.Textarea, label="Enter Rule")

class EvaluateForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea, label="Enter User Data (in JSON format)")
