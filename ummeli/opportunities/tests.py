from django.contrib.auth.models import User
from ummeli.vlive.tests.utils import VLiveClient, VLiveTestCase
from ummeli.opportunities.models import Internship, Salary


class OpportunitiesTest(VLiveTestCase):
    fixtures = [
        'vlive/tests/auth/fixtures/sample.json',
    ]

    def setUp(self):
        self.msisdn = '27123456789'
        self.pin = '1234'
        self.client = VLiveClient(HTTP_X_UP_CALLING_LINE_ID=self.msisdn)

    def test_internship(self):
        self.login()
        self.fill_in_basic_info()

        user = User.objects.get(username=self.msisdn)

        salary = Salary(amount=50, frequency=1)
        salary.save()

        Internship.objects.create(title='Test op',
                                    description='This is a test',
                                    provider=user,
                                    salary=salary)
        self.assertEqual(user.internship_set.count(), 1)
        self.assertEqual(user.internship_set.all()[0].salary.amount, 50)
        self.assertEqual(user.internship_set.all()[0].education, 0)
