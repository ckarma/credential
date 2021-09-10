from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
# from .views import ProjectDetailView

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='indexview'),
    # path('login/', views.login, name='login'),
    path('login_test/', views.login_test, name='login_test'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('djangologin/', auth_views.DjangoLoginView.as_view(), name='djangologin'),
    path('logout/', views.logout_view, name='logout'),
    path('servers/', views.ServerView.as_view(), name='servers'),
    path('projects/', views.ProjectView.as_view(), name='projects'),
    path('server/new/', views.add_server, name='add_server'),
    path('project/new/', views.add_project, name='add_project'),
    path('project/new/<int:server_id>/', views.add_project_on_server, name='add_project_on_server'),
    path('server/<int:server_id>/', views.detail, name='detail'),
    path('server/<int:server_id>/edit/', views.edit_server, name='edit_server'),
    # path('server/<int:server_id>/success/', views.detail, name='details'),
    path('project/<int:project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),

    path('add_image/', views.add_image, name='add_image')
]