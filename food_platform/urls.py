from django.urls import include, path

from .views import food_platform, foodrivers, foodonators

urlpatterns = [
    path('', food_platform.home, name='home'),

    path('foodrivers/', include(([
        path('', foodrivers.PickupListView.as_view(), name='pickup_list'),
        path('area/', foodrivers.FoodriverAreaView.as_view(), name='foodriver_area'),
        path('taken/', foodrivers.TakenPickupListView.as_view(), name='taken_pickup_list'),
        path('pickup/<int:pk>/', foodrivers.take_pickup, name='take_pickup'),
    ], 'food_platform'), namespace='foodrivers')),

    path('foodonators/', include(([
        path('', foodonators.PickupListView.as_view(), name='pickup_change_list'),
        path('pickup/add/', foodonators.PickupCreateView.as_view(), name='pickup_add'),
        path('pickup/<int:pk>/', foodonators.PickupUpdateView.as_view(), name='pickup_change'),
        path('pickup/<int:pk>/delete/', foodonators.PickupDeleteView.as_view(), name='pickup_delete'),
        path('pickup/<int:pk>/results/', foodonators.PickupResultsView.as_view(), name='pickup_results'),
        path('pickup/<int:pk>/pickup_time/add/', foodonators.pickup_time_add, name='pickup_time_add'),
        path('pickup/<int:pickup_pk>/pickup_time/<int:pickup_time_pk>/', foodonators.pickup_time_change, name='pickup_time_change'),
        path('pickup/<int:pickup_pk>/pickup_time/<int:pickup_time_pk>/delete/', foodonators.PickupTimeDeleteView.as_view(), name='pickup_time_delete'),
    ], 'food_platform'), namespace='foodonators')),
]
