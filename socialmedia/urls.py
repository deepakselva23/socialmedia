
from django.contrib import admin
from django.urls import path, include
import twitter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('twitter.urls'))
]
