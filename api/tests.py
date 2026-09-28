from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Company, KBEntry, QueryLog
class TeamBoardTests(TestCase):
    def setUp(self):
        self.client=APIClient()
        KBEntry.objects.create(question='What is select_related?',answer='Django SQL JOIN helper',category='database')
    def test_register_login_query_and_permissions(self):
        r=self.client.post('/api/auth/register/',{'username':'acme','password':'securepass123','company_name':'Acme Corp','email':'dev@acme.test'},format='json'); self.assertEqual(r.status_code,201); token=r.data['access']
        self.assertTrue(r.data['api_key'])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        q=self.client.post('/api/kb/query/',{'search':'select_related'},format='json'); self.assertEqual(q.status_code,200); self.assertEqual(q.data['count'],1); self.assertEqual(QueryLog.objects.count(),1)
        self.assertEqual(self.client.get('/api/admin/usage-summary/').status_code,403)
        c=User.objects.get(username='acme').company; c.role=Company.Role.ADMIN; c.save()
        self.assertEqual(self.client.get('/api/admin/usage-summary/').status_code,200)
    def test_no_token_query_is_401(self): self.assertEqual(self.client.post('/api/kb/query/',{'search':'x'},format='json').status_code,401)
