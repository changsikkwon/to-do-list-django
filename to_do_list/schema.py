from graphene_django.types import DjangoObjectType, ObjectType
import graphql
from .models import User, Status, ToDo
from graphql import GraphQLError

import graphene
import bcrypt
import jwt

class UserType(DjangoObjectType):
  class Meta:
    model = User
    
    
class StatusType(DjangoObjectType):
  class Meta:
    model = Status
    
    
class TodoType(DjangoObjectType):
  class Meta:
    model = ToDo
    

class Query(ObjectType):
  user = graphene.Field(UserType, id=graphene.ID())
  status = graphene.Field(StatusType, id=graphene.ID())
  todo = graphene.Field(TodoType, id=graphene.ID())
  users = graphene.List(UserType)
  
  def resolve_users(self, info, **kwargs):
    return User.objects.all()
  
  
class CreateUser(graphene.Mutation):
  class Arguments:
    account = graphene.String(required=True)
    password = graphene.String(required=True)
    
  user = graphene.Field(lambda: UserType)
  
  def mutate(self, info, account, password):
    if User.objects.filter(account=account).exists():
      raise GraphQLError('Already_Exist_Account')
    
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user = User(
      account = account,
      password = password,
    )
    
    user.save()
    
    return CreateUser(user=user)
    
        
class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()