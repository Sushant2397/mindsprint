from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_consent, name='create-consent'),
    path('<int:consent_id>/', views.get_consent, name='get-consent'),
    path('<int:consent_id>/share/', views.share_data, name='share-data'),
    path('<int:consent_id>/revoke/', views.revoke_consent, name='revoke-consent'),
]