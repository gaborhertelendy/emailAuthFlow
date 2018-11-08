from django.urls import path
from django.conf.urls import include

from .views import UsersViewSet, WorkoutsViewSet

from rest_framework import routers

admin_router = routers.DefaultRouter()
admin_router.register(r'user', UsersViewSet, base_name='user')
# router will auto generate view-names like user-list and user-details (this will user the base_name-...)
# use them in conjunction with the view-name of the root api (e.g.: api-root:user-list) see below

user_router = routers.DefaultRouter()
user_router.register('workouts', WorkoutsViewSet, base_name='workout')

app_name = 'api'
urlpatterns = [
    path('manage/', include(admin_router.urls)),  # api-root is a namespace here
    path('my/', include(user_router.urls)),  # api-root is a namespace here
]
