from django.urls import path
from django.conf import settings

from epay.views import (
    CreateSponsor,
    SponsorStatus,
    ConfirmSponsor,
    FakeSponsor,
)
urlpatterns = [
    path("confirm-sponsor/", ConfirmSponsor.as_view(), name="confirm-sponsor"),
    path("create/<str:query_params>/", CreateSponsor.as_view(), name="create-sponsor"),
    path(
        "sponsor-status/<slug:invoice_number>/",
        SponsorStatus.as_view(),
        name="sponsor-status",
    ),
path(
            "fake-sponsor/<slug:invoice_number>/",
            FakeSponsor.as_view(),
            name="fake-sponsor",
        ),
]
'''
if settings.DEBUG:
    urlpatterns = urlpatterns + [
        path(
            "fake-sponsor/<slug:invoice_number>/",
            FakeSponsor.as_view(),
            name="fake-sponsor",
        ),

    ]'''