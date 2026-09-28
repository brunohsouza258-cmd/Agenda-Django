from django.urls import path

from contact import views

app_name = 'contact'

urlpatterns = [
    path('',  views.index, name='index'),
    path('search/',  views.search, name='search'),

    # contact (CRUD)
    path('contact/<int:contact_id>/',  views.contact, name='contact'),
    path('contact/create/',  views.create, name='create'),
    path('contact/<int:contact_id>/update/',  views.Update, name='update'),
    path('contact/<int:contact_id>/Delete/',  views.Delete, name='Delete'),

    # user
        path('user/create/',  views.register, name='register'),
        path('user/login/',  views.login_view, name='login'),
        path('user/logout/',  views.logout_view, name='logout'),
        path('user/update/',  views.user_update, name='user_update'),
        ]

