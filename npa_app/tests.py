from django.test import TestCase
from rest_framework.test import APITestCase
from datetime import date
from django.contrib.auth.models import User

from customer_app.models import Customer
from loan_app.models import Loan
from npa_app.models import NPA

from npa_app.serializers import NPASerializer
from recovery_officer_app.models import RecoveryOfficer
from recovery_assignement_app.models import RecoveryAssignment


class NPATestCase(TestCase):

    def setUp(self):

        self.customer = Customer.objects.create(
            customer_code='CUST001',
            first_name='Test',
            last_name='Customer',
            email='test@example.com',
            phone='9876543210',
            address='Test Address',
            status='active'
        )

        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_account_number='LN001',
            loan_type='personal',
            sanctioned_amount=100000,
            outstanding_amount=80000,
            interest_rate=10.5,
            emi_amount=5000,
            tenure_months=24,
            sanction_date=date.today(),
            loan_status='active'
        )

    def test_create_npa(self):

        npa = NPA.objects.create(
            loan=self.loan,
            npa_date=date.today(),
            days_past_due=120,
            npa_category='substandard',
            recovery_status='pending'
        )

        self.assertIsNotNone(npa.id)

        self.assertEqual(
            npa.loan,
            self.loan
        )

        self.assertEqual(
            npa.days_past_due,
            120
        )

    def test_npa_days_past_due_validation(self):

        data = {
            'loan': self.loan.id,
            'npa_date': date.today(),
            'days_past_due': 89,
            'npa_category': 'substandard',
            'recovery_status': 'pending'
        }

        serializer = NPASerializer(data=data)

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            'days_past_due',
            serializer.errors
        )

    def test_npa_days_past_due_valid(self):

        data = {
            'loan': self.loan.id,
            'npa_date': date.today(),
            'days_past_due': 90,
            'npa_category': 'substandard',
            'recovery_status': 'pending'
        }

        serializer = NPASerializer(data=data)

        self.assertTrue(
            serializer.is_valid()
        )

class NPAAPITestCase(APITestCase):

    def test_npa_requires_authentication(self):

        response = self.client.get(
            '/api/v1/npa/'
        )

        self.assertIn(
            response.status_code,
            [401, 403]
        )

    def test_normal_user_cannot_access_npa(self):

        user = User.objects.create_user(
            username='normaluser',
            password='testpassword'
        )

        self.client.force_authenticate(
            user=user
        )

        response = self.client.get(
            '/api/v1/npa/'
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_recovery_officer_can_access_assigned_npa(self):

        # Create user
        user = User.objects.create_user(
            username='officer1',
            password='testpassword'
        )

        # Create Recovery Officer
        officer = RecoveryOfficer.objects.create(
            user=user,
            employee_id='EMP001',
            first_name='Test',
            last_name='Officer',
            email='officer@example.com',
            phone='9876543211',
            designation='Recovery Officer',
            region='Pune',
            status='active'
        )

        # Create customer
        customer = Customer.objects.create(
            customer_code='CUST002',
            first_name='Test',
            last_name='Customer',
            email='customer2@example.com',
            phone='9876543212',
            address='Test Address',
            status='active'
        )

        # Create loan
        loan = Loan.objects.create(
            customer=customer,
            loan_account_number='LN002',
            loan_type='personal',
            sanctioned_amount=100000,
            outstanding_amount=80000,
            interest_rate=10.5,
            emi_amount=5000,
            tenure_months=24,
            sanction_date=date.today(),
            loan_status='npa'
        )

        # Create NPA
        npa = NPA.objects.create(
            loan=loan,
            npa_date=date.today(),
            days_past_due=120,
            npa_category='substandard',
            recovery_status='pending'
        )

        # Assign NPA to officer
        RecoveryAssignment.objects.create(
            npa=npa,
            recovery_officer=officer,
            assigned_date=date.today(),
            assignment_status='active'
        )

        # Authenticate as Recovery Officer
        self.client.force_authenticate(
            user=user
        )

        # Call API
        response = self.client.get(
            '/api/v1/npa/'
        )

        # Check response
        self.assertEqual(
            response.status_code,
            200
        )

        # Check assigned NPA is present
        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]['id'],
            npa.id
        )