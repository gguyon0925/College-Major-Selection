from django.apps import apps

from rest_framework import serializers

from .models import CustomUser, UserProfile, Interest, Strength, Weakness, TestResult, JobRecommendation


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio',
                  'job_security_preference', 'expected_income']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'interests', 'strengths', 'weaknesses']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']


class StrengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strength
        fields = ['id', 'name']


class WeaknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weakness
        fields = ['id', 'name']


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test_name', 'score', 'date_taken']


class JobRecommendationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(JobRecommendationSerializer, self).__init__(*args, **kwargs)
        Major = apps.get_model('major_advisor', 'Major')
        self.fields['major_related'] = serializers.SlugRelatedField(
            slug_field='name',
            queryset=Major.objects.all(),
            allow_null=True,
            required=False
        )

    class Meta:
        model = JobRecommendation
        fields = ['id', 'user', 'job_title', 'major_related',
                  'recommendation_reason', 'date_recommended']
