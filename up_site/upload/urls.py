from django.urls import path

from .views import IndexView, ImageView, add_image

app_name = 'upload'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('add_image/', add_image, name="add_image"),
    path('image/<int:pk>/', ImageView.as_view(), name="image"),

]
