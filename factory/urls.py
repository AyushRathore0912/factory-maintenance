from django.contrib import admin
from django.urls import path
from maintenance.views import user_logout

from maintenance.views import (
    dashboard,
    UserLoginView,
    user_logout,
    report_breakdown,
    active_breakdowns,
    register,
    resolve_breakdown,

)


urlpatterns = [

    path("admin/", admin.site.urls),

    path(
        "login/",
        UserLoginView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        user_logout,
        name="logout"
    ),

    path(
        "breakdown/",
        report_breakdown,
        name="report_breakdown"
    ),

    path(
    "breakdowns/",
    active_breakdowns,
    name="active_breakdowns"
),

    path(
    "breakdown/resolve/<int:breakdown_id>/",
    resolve_breakdown,
    name="resolve_breakdown"
),

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path("register/", register, name="register"),
]