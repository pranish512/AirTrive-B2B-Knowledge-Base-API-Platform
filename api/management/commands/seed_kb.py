from django.core.management.base import BaseCommand
from api.models import KBEntry
DATA=[
('What is select_related in Django ORM?','select_related performs a SQL JOIN and fetches related foreign-key objects in one query.','database'),
('When should I use prefetch_related?','Use prefetch_related for many-to-many and reverse relations; it performs separate queries and joins in Python.','database'),
('How does transaction.atomic() work?','transaction.atomic groups database operations into one transaction that commits together or rolls back on error.','database'),
('What are Q objects in Django?','Q objects build complex queries using OR, AND and NOT conditions.','framework'),
('How do I use JWT authentication?','A JWT access token is sent in the Authorization header using the Bearer scheme.','api'),
('What is a REST API?','A REST API exposes resources over HTTP using methods such as GET, POST, PUT and DELETE.','api'),
('What is database indexing?','An index can speed up reads by providing an optimized lookup structure, with storage and write overhead.','database'),
('What is Docker used for?','Docker packages an application and its dependencies into portable containers.','cloud'),
('What is horizontal scaling?','Horizontal scaling adds more application instances or servers to distribute load.','cloud'),
('What is Django middleware?','Middleware is a hook layer that processes Django requests and responses globally.','framework'),
('How should API secrets be stored?','Keep credentials outside source code, for example in environment variables or a managed secret store.','general'),
]
class Command(BaseCommand):
    help='Seed at least 10 TeamBoard KB entries'
    def handle(self,*args,**opts):
        created=0
        for q,a,c in DATA:
            _,was=KBEntry.objects.get_or_create(question=q,defaults={'answer':a,'category':c}); created+=int(was)
        self.stdout.write(self.style.SUCCESS(f'Seed complete. Added {created}; total={KBEntry.objects.count()}'))
