from django.contrib import admin
from django.urls import path, include
from prediction.views import home  # ✅ Import home view for direct routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('prediction.urls')),  # ✅ API available at `/api/predict/`
    path('', home, name='home'),  # ✅ Ensure home page loads at `/`
]
