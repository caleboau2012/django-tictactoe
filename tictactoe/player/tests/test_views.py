from django.urls import reverse
from player.models import Invitation
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class InvitationViewTestCase(TestCase):
    def setUp(self):
        self.user1 = {
            "username": "user1",
            "email": "email1@test.com",
            "password": "valid_password1",
        }
        self.user2 = {
            "username": "user2",
            "email": "email2@test.com",
            "password": "valid_password2",
        }
        self.client = Client()

        User.objects.create_user(
            self.user1["username"], self.user1["email"], self.user1["password"]
        )
        User.objects.create_user(
            self.user2["username"], self.user2["email"], self.user2["password"]
        )

    def test_invitation_get(self):
        url = reverse("player_new_invitation")
        self.client.login(
            username=self.user1["username"], password=self.user1["password"]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Send the invitation")

    def test_invitation_post(self):
        url = reverse("player_new_invitation")
        user1 = User.objects.get_by_natural_key(self.user1["username"])
        user2 = User.objects.get_by_natural_key(self.user2["username"])
        data = {"from_user": user1.id, "to_user": user2.id}
        self.client.login(
            username=self.user1["username"], password=self.user1["password"]
        )

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("player_home"))
        self.assertEqual(Invitation.objects.count(), 1)

    def test_accept_invitation_get(self):
        user1 = User.objects.get_by_natural_key(self.user1["username"])
        user2 = User.objects.get_by_natural_key(self.user2["username"])
        invitation = Invitation()
        invitation.from_user = user1
        invitation.to_user = user2
        invitation.save()

        url = reverse("player_accept_invitation", kwargs={"id": 1})
        self.client.login(
            username=self.user2["username"], password=self.user2["password"]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("player/accept_invitation_form.html")

    def test_accept_invitation_request_guard(self):
        user1 = User.objects.get_by_natural_key(self.user1["username"])
        user2 = User.objects.get_by_natural_key(self.user2["username"])
        invitation = Invitation()
        invitation.from_user = user1
        invitation.to_user = user2
        invitation.save()

        url = reverse("player_accept_invitation", kwargs={"id": 1})
        self.client.login(
            username=self.user1["username"], password=self.user1["password"]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_accept_invitation_post(self):
        user1 = User.objects.get_by_natural_key(self.user1["username"])
        user2 = User.objects.get_by_natural_key(self.user2["username"])
        invitation = Invitation()
        invitation.from_user = user1
        invitation.to_user = user2
        invitation.save()

        url = reverse("player_accept_invitation", kwargs={"id": 1})
        self.client.login(
            username=self.user2["username"], password=self.user2["password"]
        )
        data = {"accept": "ok"}

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("gameplay_detail", kwargs={"id": 1}))
        self.assertEqual(Invitation.objects.count(), 0)

    def test_deny_invitation_post(self):
        user1 = User.objects.get_by_natural_key(self.user1["username"])
        user2 = User.objects.get_by_natural_key(self.user2["username"])
        invitation = Invitation()
        invitation.from_user = user1
        invitation.to_user = user2
        invitation.save()

        url = reverse("player_accept_invitation", kwargs={"id": 1})
        self.client.login(
            username=self.user2["username"], password=self.user2["password"]
        )
        data = {"deny": "no"}

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("player_home"))
        self.assertEqual(Invitation.objects.count(), 0)
