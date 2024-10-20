from django.urls import path
from . import views

urlpatterns = [
    path('create-rule/', views.create_rule_view, name='create_rule_view'),
    path('combine-rules/', views.combine_rules_view, name='combine_rules_view'),
    path('evaluate-rule/', views.evaluate_rule_view, name='evaluate_rule_view'),
    path('list-rules/', views.list_rules_view, name='list_rules_view'),
]
