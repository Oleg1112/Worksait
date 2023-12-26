"""
Definition of urls for PskovskiyFootball.
"""

from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('store/', views.store, name= 'store'),
    path('courses/', views.courses, name= 'courses'),
    path('course/<int:parametr>/', views.course, name='course'),
    path('courses/enroll/', views.enroll, name= 'enroll'),
    path('store/', views.store, name= 'store'),
    path('product/<int:parametr>/',views.product, name= 'product'),
    path('store/buy/', views.store_buy, name= 'store_buy'),
    path('store/cancel/', views.store_cancel, name= 'store_cancel'),
    path('store/dec/', views.store_dec, name= 'store_dec'),
    path('store/inc/', views.store_inc, name= 'store_inc'),
    path('store/place/', views.store_place, name= 'store_place'),
    path('cart/', views.cart, name= 'cart'),
    path('profile/', views.profile, name= 'profile'),
    path('registration/',views.registration, name= 'registration'),
    path('management/', views.management, name= 'management'),
    path('management/orders', views.manage_orders, name= 'manage_orders'),
    path('management/enrollments', views.manage_enrollments, name= 'manage_enrollments'),
    path('management/blog', views.manage_blog, name= 'manage_blog'),
    path('management/newpost', views.manage_new_post, name= 'manage_new_post'),
    path('management/products', views.manage_products, name= 'manage_products'),
    path('management/newproduct', views.manage_new_product, name= 'manage_new_product'),
    path('management/courses', views.manage_courses, name= 'manage_courses'),
    path('management/newcourse', views.manage_new_course, name= 'manage_new_course'),
    path('manage/order/status', views.manage_order_status, name= 'manage_order_status'),
    path('manage/enroll/status', views.manage_enrollment_status, name= 'manage_enrollment_status'),
    path('manage/blog/<int:parametr>/change', views.manage_blog_change, name= 'manage_blog_change'),
    path('manage/blog/<int:parametr>/delete', views.manage_blog_delete, name= 'manage_blog_delete'),
    path('manage/product/<int:parametr>/change', views.manage_product_change, name= 'manage_product_change'),
    path('manage/product/<int:parametr>/delete', views.manage_product_delete, name= 'manage_product_delete'),
    path('manage/course/<int:parametr>/change', views.manage_course_change, name= 'manage_course_change'),
    path('manage/course/<int:parametr>/delete', views.manage_course_delete, name= 'manage_course_delete'),
    path('login/',
         LoginView.as_view
         (
             template_name='login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += [ re_path(r'^.*', views.missing_page, name='missing_page')]
