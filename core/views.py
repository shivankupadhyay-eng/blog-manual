from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Q
from rest_framework.exceptions import PermissionDenied,ValidationError
from .models import CustomUser,Blog,Comment,Vote
from .serializers import( CustomUserCreateSerializer,CustomUserListSerializer,CustomUserUpdateSerializer,
                        LoginSerializer, BlogCreateSerializer,BlogListSerializer,BlogUpdateSerializer,
                         CommentCreateSerializer,CommentListSerializer,CommentUpdateSerializer,
                         VoteCreateSerializer,BlogVoteStatsSerializer)


class CustomUserAPIView(APIView):

    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            CustomUserListSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def get(self,request,id):
        user=get_object_or_404(CustomUser,id=id)
        serializer=CustomUserListSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def patch(self,request,id):
        user=get_object_or_404(CustomUser,id=id)
        if request.user!=user:
            raise PermissionDenied("You can update only your profile!")
        
        serializer=CustomUserUpdateSerializer(
            user,
            request.data,
            partial=True)
        
        serializer.is_valid(raise_exception=True)
        updated_user=serializer.save()
        
        return Response(
            CustomUserUpdateSerializer(updated_user).data,
            status=status.HTTP_200_OK
        )
        

    def put(self,request,id):
        user=get_object_or_404(CustomUser,id=id)
        
        if request.user!=user:
            raise PermissionDenied("You can update your profile only!")
        
        serializer=CustomUserUpdateSerializer(
            user,
            request.data,
            partial=False)
        serializer.is_valid(raise_exception=True)
        updated_user=serializer.save()

        return Response(
            CustomUserUpdateSerializer(updated_user).data,
            status=status.HTTP_200_OK
        )
        
    def delete(self,request,id):
        user=get_object_or_404(CustomUser,id=id,is_deleted=False)

        if request.user!=user:
            raise PermissionDenied("You can delete only your profile!")
        
        user.is_delete=True
        user.save()

        return Response(
            {"message":"User deactivated successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )

class LoginAPIView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        refresh=RefreshToken.for_user(user)

        return Response({
            "access":str(refresh.access_token),
            "refressh":str(refresh)
        })
    

class BlogAPIView(APIView):

    def post(self,request):
        serializer=BlogCreateSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        blog=serializer.save(
        created_by=request.user,
        updated_by=request.user
        )
        return Response(BlogCreateSerializer(blog).data,status=status.HTTP_201_CREATED)
    
    def get(self,request,id):
        blog=get_object_or_404(Blog,id=id,is_deleted=False)
        serializer=BlogListSerializer(blog)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id):
        blog=get_object_or_404(Blog,id=id)
        
        if blog.created_by!=request.user:
            raise PermissionDenied("You can only update your own blog")
        
        serializer=BlogUpdateSerializer(blog,data=request.data,partial=False)
        
        serializer.is_valid(raise_exception=True)
        updated_blog=serializer.save(updated_by=request.user)

        return Response(BlogUpdateSerializer(updated_blog).data,status=status.HTTP_200_OK)
        
    def patch(self,request,id):
        blog=get_object_or_404(Blog,id=id)
        
        if blog.created_by!=request.user:
            raise PermissionDenied("You can update only your blog")
        
        serializer=BlogUpdateSerializer(blog,data=request.data,partial=True)
        
        serializer.is_valid(raise_exception=True)
        updated_blog=serializer.save(updated_by=request.user)
        
        return Response(BlogUpdateSerializer(updated_blog).data,status=status.HTTP_200_OK)
    
    def delete(self,request,id):
        blog=get_object_or_404(Blog,id=id,is_deleted=False)
        
        if blog.created_by!=request.user:
            raise PermissionDenied("You can delete only your blog")
        
        blog.is_deleted=True
        blog.save(update_fields=["is_deleted"])
        
        return Response({"message":"Blog deleted succesfully!"},status=status.HTTP_204_NO_CONTENT)


class CommentAPIView(APIView):

    def post(self,request):
        serializer=CommentCreateSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        comment=serializer.save(
            created_by=request.user,
            updated_by=request.user
            )
        return Response(CommentCreateSerializer(comment).data,status=status.HTTP_201_CREATED)
    
    def get(self,request):
        queryset=Comment.objects.filter(is_deleted=False)

        blog_id=request.query_params.get("blog")
        if blog_id:
            queryset=queryset.filter(blog_id=blog_id)

        serializer=CommentListSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def patch(self,request,id):
        comment=get_object_or_404(Comment,id=id)

        if comment.created_by!=request.user:
            raise PermissionDenied("You can update your own comment only")
        
        serializer=CommentUpdateSerializer(comment,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id):
        comment=get_object_or_404(Comment,id=id)
        
        if comment.created_by!=request.user:
            raise PermissionDenied("You can update you blog only")

        serializer=CommentUpdateSerializer(comment,data=request.data,partial=False)

        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,id):
        comment=get_object_or_404(Comment,id=id,is_deleted=False)

        if comment.created_by!=request.user:
            raise PermissionDenied("You can delete only your own comment")
        
        comment.is_deleted=True
        comment.save(update_fields=["is_deleted"])

        return Response({"message":"Comment deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    

class VoteAPIView(APIView):

    def post(self,request,blog_id):
        blog=get_object_or_404(Blog,id=blog_id,is_deleted=False)

        serializer=VoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vote_value=serializer.validated_data["value"]

        if vote_value not in [1,-1]:
            raise ValidationError("Vote value must be 1 or -1")

        vote,created=Vote.objects.update_or_create(
            blog=blog,
            user=request.user,
            defaults={"value":vote_value}
        )
        return Response(
            {
               "message":"Vote recorded",
               "vote":vote.value 
            },
            status=status.HTTP_200_OK
        )

    def delete(self,request,blog_id):
        blog=get_object_or_404(Blog,id=blog_id,is_deleted=False)
        
        deleted,_ = Vote.objects.filter(
            blog=blog,
            user=request.user
        ).delete()

        if deleted == 0:
            return Response(
                {"message":"No vote to remove"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message":"Vote removed"},
            status=status.HTTP_204_NO_CONTENT
        )


class BlogVoteStatsAPIView(APIView):

    def get(self,request):
        blogs = Blog.objects.annotate(
            upvotes=Count("votes", filter=Q(votes__value=1)),
            downvotes=Count("votes", filter=Q(votes__value=-1)),
            score=Sum("votes__value"),)
        serializer = BlogVoteStatsSerializer(blogs,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogVoteDetailAPIView(APIView):

    def get(self, request, id):
        blog = (
            Blog.objects
            .filter(id=id)
            .annotate(
                upvotes=Count("votes", filter=Q(votes__value=1)),
                downvotes=Count("votes", filter=Q(votes__value=-1)),
                score=Sum("votes__value"),
            )
            .first()
        )

        serializer = BlogVoteStatsSerializer(blog)
        return Response(serializer.data)
