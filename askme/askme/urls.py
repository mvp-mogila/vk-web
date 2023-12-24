"""
URL configuration for askme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from app import views
from . import settings


urlpatterns = [
    path('', views.index_handler, name = "index"),
    path('new', views.new_questions_handler, name = "new"),
    path('hot', views.hot_questions_handler, name = "hot"),
    path('signup', views.signup_handler, name = "signup"),
    path('login', views.login_handler, name = "login"),
    path('profile/<str:username>', views.profile_handler, name = "profile"),
    path('logout', views.logout_handler, name = "logout"),
    path('ask', views.ask_handler, name = "ask"),
    path('question/<int:question_id>', views.question_handler, name = "question"),
    path('answer/vote', views.answer_vote_handler, name = "answer_vote"),
    path('question/vote', views.question_vote_handler, name = "question_vote"),
    path('tag/<str:tag_name>', views.tag_handler, name = "tag"),
    path('admin/', admin.site.urls, name = "admin"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)