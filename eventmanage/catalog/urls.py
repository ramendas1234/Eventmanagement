from django.urls import path
from catalog import views 


urlpatterns = [
    path('', views.index, name='index'),
    #path('books/', views.BookListView.as_view(), name='books'),
    path('<str:city>/', views.location_based_events, name='city-list'),
    path('<str:city>/event-filter/',views.event_filtration)
    # path('abc/', views.test, name='city-list'),
]