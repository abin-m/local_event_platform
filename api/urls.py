from django.urls import path
from .views import event_list, UserRegistration, UserLogin

urlpatterns = [
   
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('events/', event_list, name='event-list'),
    path('events/<int:pk>/', event_list, name='event-detail'),
]
