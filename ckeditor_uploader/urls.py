from __future__ import absolute_import

from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from . import views


# removed the >1.8 check

urlpatterns = [
    url(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
    url(r'^browse/', login_required(views.browse), name='ckeditor_browse'),
]

