from django.contrib.sites.models import Site

first_site = Site.objects.all()[0]
first_site.domain = 'salvetempo.com'
first_site.name = 'SalveTempo'
first_site.save()