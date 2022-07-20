from django.urls import path
from pn_queries import views

app_name = "pn_queries"
urlpatterns = [
    path('', views.all_pn_queries_view, name="pn_queries"), 
]
