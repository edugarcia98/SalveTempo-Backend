from django.contrib.sites.models import Site

first_site = Site.objects.all()[0]
first_site.domain = '192.168.1.21:8000'
first_site.name = 'SalveTempo'
first_site.save()