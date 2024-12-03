from django.urls import path
from . import views

app_name = 'medicall'  # This allows you to use `{% url 'medicall:index' %}` in templates
urlpatterns = [
    path('', views.index, name='index'),  # Ensure the `name` matches what you're reversing in the template
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('show_appointments/',views.retrieve_appointments,name="show_appointments"),
    path('delete/<int:id>',views.delete_appointment,name="delete_appointment"),
    path('update_appointment/<int:id>/', views.update_appointment, name='update_appointment'),

    path('upload/',views.upload_image,name='upload_image'),
    # Add the <int:id> argument to the pay URL
    path('pay/<int:id>/', views.pay, name='pay'),  # Expect an ID in the URL
    
    # Other URL patterns
    path('stk/', views.stk, name='stk'),  # send the stk push prompt
    path('token/', views.token, name='token'),  # generate the token for that particular transaction
]


