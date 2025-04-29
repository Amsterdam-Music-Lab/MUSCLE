"""aml URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# Admin strings
admin.site.site_header = "AML Admin"
admin.site.site_title = "AML Admin"
admin.site.index_title = "Welcome to AML Admin"

# Urls patterns
urlpatterns = [
    path("experiment/", include("experiment.urls")),
    path("question/", include("question.urls")),
    path("participant/", include("participant.urls")),
    path("result/", include("result.urls")),
    path("section/", include("section.urls")),
    path("session/", include("session.urls")),
    path("theme/", include("theme.urls")),
    path("admin_interface/", include("admin_interface.urls")),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Sentry debug (uncomment to test Sentry)
    # path('sentry-debug/', lambda request: 1 / 0),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#   ^ The static helper function only works in debug mode
# (https://docs.djangoproject.com/en/3.0/howto/static-files/)


# Prefix all URLS with /server if AML_SUBPATH is set
if settings.SUBPATH:
    urlpatterns = [path("server/", include(urlpatterns))]

# Debug toolbar
if settings.DEBUG and not settings.TESTING:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
