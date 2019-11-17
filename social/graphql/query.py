import graphene
from django.db import models
from django.contrib.auth.models import User
from graphene import Field, List, Int, ID, NonNull, ObjectType
from graphene_django import DjangoObjectType
from .types import PostType, CommentType, LikeType
from ..models import Post, Comment, Like


class GetPostQuery(ObjectType):
    post = Field(PostType, post_id=ID())

    def resolve_post(self, info, post_id):
        return Post.objects.get(id=post_id)


class GetPostCommentsQuery(ObjectType):
    post_comments = List(CommentType, post_id=ID(
    ), offset=Int(default_value=0), limit=Int(default_value=20))

    def resolve_post_comments(self, info, post_id, offset, limit):
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post_id)
        return comments.distinct()[offset:offset+limit]


class GetPostLikesQuery(ObjectType):
    post_likes = List(LikeType, post_id=ID(
    ), offset=Int(default_value=0), limit=Int(default_value=20))

    def resolve_post_like(self, info, post_id, offset, limit):
        post = Post.objects.get(id=post_id)
        likes = Like.objects.filter(post=post_id)
        return likes.distinct()[offset:offset+limit]


# GetPostLikesCount


class PostsQuery(ObjectType):
    posts = NonNull(List(PostType))
    # Depricated: Replace with auth_user Friend list posts

    def resolve_posts(self, info):
        return Post.objects.all()
