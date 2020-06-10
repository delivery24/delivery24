import pytest
import pytest_django

from django.urls import reverse, resolve
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render

from accounts.views import signup
from accounts.models import User
from accounts.tokens import account_activation_token

from django.test.client import Client

class TestViews:
    # Test /accounts/login/
    def test_login_view_status_code(self, client):
        url = reverse('accounts:login')
        response = client.get(url)
        assert response.status_code is 200

    def test_login_url_resolves_login_view(self):
        view = resolve('/accounts/login/')
        assert view.func.__name__ == LoginView.as_view().__name__

    # Test /accounts/signup/
    def test_signup_view_status_code(self, client):
        url = reverse('accounts:signup')
        response = client.get(url)
        assert response.status_code is 200

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        assert view.func.__name__ == signup.__name__

    # Test /accounts/logout/
    @pytest.mark.django_db
    def test_logout_view_status_code(self, client):
        url = reverse('accounts:logout')
        response = client.get(url)
        assert response.status_code is HttpResponseRedirect.status_code

    @pytest.mark.django_db
    def test_logout_redirects_to_index(self, client):
        url = reverse('accounts:logout')
        response = client.get(url)
        assert response.url == reverse('core:index')

    def test_logout_url_resolves_logout_view(self):
        view = resolve('/accounts/logout/')
        assert view.func.__name__ == LogoutView.as_view().__name__


@pytest.mark.django_db
class TestSignUp:
    url = reverse('accounts:signup')
    data = {
        'email': 'john@mail.ee',
        'first_name': 'john',
        'last_name': 'doe',
        'ik': 12345,
        'phone_0': 55478,
        'phone_1': 371,
        'car_model': 'vw',
        'car_carrying': 1000,
        'car_number': '123abc',
        'payment': 1,
        'password1': 'abcdef123456',
        'password2': 'abcdef123456'
    }

    def test_empty_form(self, client):
        resp = client.post(self.url, {})
        assert resp.status_code == 200

    def test_correct_signup(self, client, mailoutbox):
        resp = client.post(self.url, self.data)
        assert resp.status_code == HttpResponseRedirect.status_code
        assert resp.url == reverse('accounts:account_activation_sent')

        # Test sent email
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        subject = 'Activate Your delivery24.ee Account'
        assert mail.subject == subject
        assert mail.to == [self.data['email']]
        assert User.objects.exists() is True

        # Test activation link
        user = User.objects.get(pk=1)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        server_name = 'testserver'
        activation_url = f"http://{server_name}" \
                         f"{reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})}"
        assert activation_url in mail.body

        # Test activation link first click
        first_resp = client.get(activation_url)
        assert first_resp.status_code == HttpResponseRedirect.status_code
        assert first_resp.url == reverse('core:index')

        # Test activation link second click
        second_resp = client.get(activation_url)
        assert second_resp.status_code == 200
        exp_resp = render(resp.request, 'accounts/account_activation_invalid.html')
        assert exp_resp.content == second_resp.content
