from django.contrib import admin
from django.urls import include, path
from food_platform.views import food_platform, foodrivers, foodonators


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food_platform.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', food_platform.SignUpView.as_view(), name='signup'),
    path('accounts/signup/foodriver/', foodrivers.FoodriverSignUpView.as_view(), name='foodriver_signup'),
    path('accounts/signup/foodonator/', foodonators.FoodonatorSignUpView.as_view(), name='foodonator_signup'),
    # path('accounts/signup/shelters/', shelters.TeacherSignUpView.as_view(), name='shelter_signup'),

]
