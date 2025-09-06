from django.urls import path
from . import views

urlpatterns = [
    path('groups/<int:group_id>/compute_settlement/', views.compute_settlement, name='compute-settlement'),
    path('groups/<int:group_id>/settlement_graph/', views.get_settlement_graph, name='settlement-graph'),
]