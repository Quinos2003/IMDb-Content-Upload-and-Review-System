from django.db import models

class Movie(models.Model):
    budget = models.FloatField(null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.FloatField(null=True, blank=True)
    production_company_id = models.IntegerField(null=True, blank=True)
    genre_id = models.IntegerField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)  # To store the list of languages
