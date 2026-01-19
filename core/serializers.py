from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Blog,CustomUser,Comment,Vote


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    phone_number=serializers.CharField(required=True)

    class Meta:
        model=CustomUser
        fields=['phone_number','email','first_name','profile_picture','password']
        
    def create(self,validated_data):
        return CustomUser.objects.create_user(**validated_data)

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','first_name','profile_picture']

class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["id",
            "phone_number",
            "email",
            "first_name",
            "profile_picture"]
    
class LoginSerializer(serializers.Serializer):
    phone_number=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        user=authenticate(
            phone_number=data["phone_number"],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user']=user
        return data

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['content','blog']
    
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"
    
class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['content']

class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=['title','picture','description']

class BlogListSerializer(serializers.ModelSerializer):
    comments=CommentListSerializer(many=True,read_only=True)
    class Meta:
        model=Blog
        fields="__all__"
    
class BlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=['title','picture','description']


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields=['value']
    

class BlogVoteStatsSerializer(serializers.ModelSerializer):
    upvotes = serializers.IntegerField(read_only=True)
    downvotes = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Blog
        fields = ['id','title','upvotes','downvotes','score']
