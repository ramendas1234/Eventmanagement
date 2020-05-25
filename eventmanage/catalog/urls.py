from django.urls import path
from catalog import views 



urlpatterns = [
    path('', views.index, name='index'),
    #path('books/', views.BookListView.as_view(), name='books'),
    path('events/', views.all_events, name='events'),
    path('events/filter/', views.all_events_filter, name='events-filter'),
    path('event/<int:pk>/',views.EventDetailView.as_view(), name='event-detail'),
    path('signup/',views.signup_view,name='signup'),
    path('signin/',views.signin_view,name='signin'),
    path('profile/<str:queryvar>/',views.view_dashboard,name='dashboard'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
	path('logout/', views.logout, name='logout'),

    path('abc/', views.test, name='test'),

    path('<str:city>/', views.location_based_events, name='city-list'),
    path('<str:city>/event-filter/',views.event_filtration),
    
    
    
]
