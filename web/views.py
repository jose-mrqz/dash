from django.contrib.auth.mixins import LoginRequiredMixin
import django.contrib.auth.views as auth_views
from django.contrib.auth import authenticate, login
from core import models
import requests
from typing import Any
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
import msal
from django.conf import settings
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView

msal_app = msal.ConfidentialClientApplication(
    client_id=settings.PBI_CLIENT_ID,
    client_credential=settings.PBI_CLIENT_SECRET,
    authority=settings.PBI_AUTHORITY
)

class AzureLoginView(TemplateView):
    template_name = 'auth/azure/login.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['auth_url'] = msal_app.get_authorization_request_url(
            scopes=settings.PBI_SCOPES,
            redirect_uri=settings.PBI_REDIRECT_URI,
        )
        return context


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        return auth_views.logout_then_login(
            request, login_url=reverse_lazy("web:login")
        )

class AzureLoginCallbackView(View):
    def get(self, request, *args, **kwargs):
        code = self.request.GET['code']
        result = msal_app.acquire_token_by_authorization_code(
            code=code,
            scopes=settings.PBI_SCOPES,
            redirect_uri=settings.PBI_REDIRECT_URI
        )
        valid_login = True
        if 'id_token_claims' in result:
            email = result['id_token_claims']['preferred_username']
            domain = email.split('@')[1]
            username = email.split('@')[0]
            if domain != 'plazasanmiguel.com.pe':
                valid_login = False
        if "access_token" in result and valid_login:
            user = models.User.objects.filter(username=username).first()
            if not user:
                user = models.User.objects.create_user(username=username, password='2020$psm', email=email)
            url= reverse_lazy('web:report', kwargs={'report_id': 2})
            login(request, user)
            self.request.session["access_token"] = result["access_token"]
            self.request.session["refresh_token"] = result["refresh_token"]
            return redirect(url)
        else:
            return redirect(reverse_lazy('web:login'))

class ReportView(LoginRequiredMixin, DetailView):
    template_name = 'report.html'
    model = models.Report
    pk_url_kwarg = 'report_id'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        result = msal_app.acquire_token_by_refresh_token(self.request.session['refresh_token'], scopes=settings.PBI_SCOPES)
        self.request.session['access_token'] = result['access_token']
        report: models.Report = self.get_object()
        access_token = self.request.session["access_token"]
        url = f'https://api.powerbi.com/v1.0/myorg/reports/{report.report_id}'
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        json_response = response.json()
        context.update({
            'access_token': self.request.session['access_token'],
            'embed_url': json_response['embedUrl']
        })
        return context
