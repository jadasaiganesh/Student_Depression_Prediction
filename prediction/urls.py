from django.urls import path
from .views import home, predict_depression

urlpatterns = [
    path('', home, name='home'),  # ✅ Home page
    path('predict/', predict_depression, name='predict_depression'),  # ✅ API route
]

