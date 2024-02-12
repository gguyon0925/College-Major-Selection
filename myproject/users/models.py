from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    job_security_preference = models.CharField(max_length=10, choices=[(
        'HIGH', 'High'), ('LOW', 'Low'), ('MEDIUM', 'medium')], default='HIGH')
    expected_income = models.IntegerField(blank=True, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    interests = models.ManyToManyField('Interest', blank=True)
    strengths = models.ManyToManyField('Strength', blank=True)
    weaknesses = models.ManyToManyField('Weakness', blank=True)


class Interest(models.Model):
    name = models.CharField(max_length=100)


class Strength(models.Model):
    name = models.CharField(max_length=100)


class Weakness(models.Model):
    name = models.CharField(max_length=100)


class TestResult(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='test_results')
    test_name = models.CharField(max_length=100)
    score = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_taken']

    def __str__(self):
        return f"{self.user.username} - {self.test_name} - {self.score}"


class JobRecommendation(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='job_recommendations')
    job_title = models.CharField(max_length=100)
    major_related = models.ForeignKey(
        'major_advisor.Major', on_delete=models.SET_NULL, null=True, blank=True)
    recommendation_reason = models.TextField()
    date_recommended = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_recommended']

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"
