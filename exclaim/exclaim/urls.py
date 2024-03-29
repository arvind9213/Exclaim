"""exclaim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from posts import urls as posts_url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from posts import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/',include(posts_url,namespace="posts")),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/posts/'}, name='logout'),
    url(r'^register/$',views.user_register,name='register')

]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

