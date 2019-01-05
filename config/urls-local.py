from django.contrib import admin
from django.urls import path, include

from .urls import *
from .settings.local import DEBUG


if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
