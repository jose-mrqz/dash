from django.urls import path
from django.urls.base import reverse_lazy
from django.views.generic.base import RedirectView
from web import views

app_name = "web"

urlpatterns = (
    path("", RedirectView.as_view(url=reverse_lazy("web:login"))),
    path("login/", views.AzureLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("azure-callback/", views.AzureLoginCallbackView.as_view(), name="azure_callback"),
    path("<int:report_id>/report/", views.ReportView.as_view(), name="report"),
)
