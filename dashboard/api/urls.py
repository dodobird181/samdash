"""URL patterns for the dashboard API."""
from django.urls import path
from dashboard.api import views

urlpatterns = [
    path("widgets/", views.widget_list, name="api-widgets"),
    path("shortcuts/", views.shortcut_list, name="api-shortcuts"),
    path("gold-price/", views.gold_price, name="api-gold-price"),
    path("silver-price/", views.silver_price, name="api-silver-price"),
    path("oil-price/", views.oil_price, name="api-oil-price"),
    path("treasury-10y/", views.treasury_10y, name="api-treasury-10y"),
    path("dow-gold-ratio/", views.dow_gold_ratio, name="api-dow-gold-ratio"),
]
