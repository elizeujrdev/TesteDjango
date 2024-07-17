from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, views_htmx
from .utilities import app_name as apn



class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name']=apn
        context['page_title']= f'{apn} | Login'
        context['title']=f'{apn} | Login'

        context['host_path']='Login'
        context['custom_variable'] = 'Valor personalizado'
        return context


urlpatterns = [
    path('', views.home,name='home'),
    path('etl/', views.etl,name='etl'),
    path('action_detail/', views.action_detail,name='action_detail'),
    path('notifications/', views.notifications,name='notifications'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("action_detail/<int:id>/", views.action_detail,name='action_detail'),
    path("refresh_action_link/<int:id>/", views_htmx.refresh_action_link,name='refresh_action_link')
]




htmx_urlpatterns = [
    path("add_action/", views_htmx.add_action,name='add_action'),
]

urlpatterns += htmx_urlpatterns




