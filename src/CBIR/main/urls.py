from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index_view, name='main'),
    path('uploadimage/', views.upload_form_img_input, name='step1'),
    path('uploaddataset/', views.upload_form_dataset, name='step2'),
    path('searchimage/', views.display_result, name='display-result'),
    path('changeimage/', views.change_image, name='change-image'),
    path('changedataset/', views.change_dataset, name='change-dataset'),
    path('how-to-use/', views.display_result, name='howtouse'),
    path('learn-more/', views.display_result, name='learnmore'),
    path('about-us/', views.display_result, name='aboutus'),
]
