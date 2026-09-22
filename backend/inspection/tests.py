"""写权限收口测试：只读账号三处（顶栏入口、登记页、提交）全部被挡，
持灯账号登记一盏光强充足的灯仍然成功。"""
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from inspection.models import Inspection


class WriteGateTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="inspector")
        self.keeper = User.objects.create_user(username="keeper", password="light123456")
        self.keeper.groups.add(self.group)
        self.watch = User.objects.create_user(username="watch", password="watch123456")
        self.bright_light = {
            "aid_code": "LH-77",
            "measured_cd": "1500",
            "required_cd": "1200",
            "bearing_error_deg": "0",
        }

    # ---- 只读账号：被拒，行数不变 ----

    def test_reader_nav_has_no_register_link(self):
        self.client.force_login(self.watch)
        resp = self.client.get(reverse("list"))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, reverse("create"))

    def test_reader_create_page_denied_without_new_row(self):
        self.client.force_login(self.watch)
        before = Inspection.objects.count()
        resp = self.client.get(reverse("create"))
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Inspection.objects.count(), before)

    def test_reader_submit_denied_without_new_row(self):
        self.client.force_login(self.watch)
        before = Inspection.objects.count()
        resp = self.client.post(reverse("create"), self.bright_light)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Inspection.objects.count(), before)

    # ---- 持灯账号：登记成功，行数加一 ----

    def test_keeper_nav_has_register_link(self):
        self.client.force_login(self.keeper)
        resp = self.client.get(reverse("list"))
        self.assertContains(resp, reverse("create"))

    def test_keeper_submit_bright_light_creates_row(self):
        self.client.force_login(self.keeper)
        before = Inspection.objects.count()
        resp = self.client.post(reverse("create"), self.bright_light)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Inspection.objects.count(), before + 1)
        row = Inspection.objects.get(aid_code="LH-77")
        self.assertEqual(row.verdict, "合格")
        self.assertRedirects(resp, reverse("detail", args=[row.pk]))
