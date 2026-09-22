from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from inspection.models import Inspection


class RegisterGateTests(TestCase):
    def setUp(self):
        self.inspector_group = Group.objects.create(name="inspector")
        self.keeper = User.objects.create_user(username="keeper", password="light123456")
        self.keeper.groups.add(self.inspector_group)
        self.watch = User.objects.create_user(username="watch", password="watch123456")
        self.valid_payload = {
            "aid_code": "LH-77",
            "measured_cd": "1400",
            "required_cd": "1200",
            "bearing_error_deg": "0.4",
        }

    # ---- 只读账号：顶栏、登记页、提交三处全部挡住 ----

    def test_reader_has_no_register_nav_link(self):
        self.client.force_login(self.watch)
        resp = self.client.get(reverse("list"))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'href="/inspections/new/"')

    def test_reader_create_page_forbidden(self):
        self.client.force_login(self.watch)
        resp = self.client.get(reverse("create"))
        self.assertEqual(resp.status_code, 403)

    def test_reader_submit_rejected_and_row_count_unchanged(self):
        self.client.force_login(self.watch)
        before = Inspection.objects.count()
        resp = self.client.post(reverse("create"), self.valid_payload)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Inspection.objects.count(), before)

    # ---- 持灯巡检员：光强充足的灯必须登记成功 ----

    def test_keeper_has_register_nav_link(self):
        self.client.force_login(self.keeper)
        resp = self.client.get(reverse("list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'href="/inspections/new/"')

    def test_keeper_create_page_open(self):
        self.client.force_login(self.keeper)
        resp = self.client.get(reverse("create"))
        self.assertEqual(resp.status_code, 200)

    def test_keeper_submit_succeeds_and_row_count_increments(self):
        self.client.force_login(self.keeper)
        before = Inspection.objects.count()
        resp = self.client.post(reverse("create"), self.valid_payload)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Inspection.objects.count(), before + 1)
        row = Inspection.objects.get(aid_code="LH-77")
        self.assertEqual(row.verdict, "合格")
        self.assertEqual(row.created_by, "keeper")
