from django.urls import path
from catalog import views 



urlpatterns = [
    path('', views.index, name='index'),
    #path('books/', views.BookListView.as_view(), name='books'),
    path('category/<int:pk>/', views.EventListView.as_view(), name='events-category'),
    path('events/', views.all_events, name='events'),
    path('events/filter/', views.all_events_filter, name='events-filter'),
    path('event/<int:pk>/',views.EventDetailView.as_view(), name='event-detail'),
    path('signup/',views.signup_view,name='signup'),
    path('signin/',views.signin_view,name='signin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/<str:queryvar>/',views.view_dashboard,name='profile-update'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
	path('logout/', views.logout, name='logout'),
    path('attendee_process/', views.attendee_process, name='attendee_process'),
    path('checkout/', views.checkout_process, name='checkout_process'),
    path('payment-redirect/',views.payment_render,name="payment-redirect"),
    path('success/',views.success,name="success"),
    path('failure/',views.failure,name="failure"),
    path('abc/', views.test, name='test'),

    path('<str:city>/', views.location_based_events, name='city-list'),
    path('<str:city>/event-filter/',views.event_filtration),
    
    
    
]
