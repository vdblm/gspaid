from financial.models import *
from authorization.models import *

Currency.objects.create(name='EUR')
Currency.objects.create(name='USD')
Currency.objects.create(name='IRR')

SuperUser.objects.create_user(username="site")
User.objects.create_superuser(username="manager", password="salamhavij", email="vbmeresht1997@gmail.com")
