from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
# ضيف السطر ده فوق مع باقي الـ imports في أول الملف
from .models import Task, Category

# وضيف الكود ده تحت خالص بعد السطر 23
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color'] 

class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('id', 'username', 'email')
class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user','created_at','updated_at') # اليوزر مش هيكتبه، السيستم اللي بيحدده

    def create(self, validated_data):
        # بنربط المهمة باليوزر اللي عمل الطلب فوراً
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)