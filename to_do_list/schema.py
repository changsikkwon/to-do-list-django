from graphene_django.types import DjangoObjectType, ObjectType
from .models import User, Status, ToDo
from graphql import GraphQLError
from .utils import login_required
from django_globals import globals

import graphene
import bcrypt
import jwt
import config

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

  
class AuthUser(graphene.Mutation):
  class Arguments:
    account = graphene.String(required=True)
    password = graphene.String(required=True)
    
  access_token = graphene.Field(graphene.String)
  
  def mutate(self, info, account, password):
    user = User.objects.get(account=account)
    
    if user:
      if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = jwt.encode({'user_id' : user.id}, config.SECRET_KEY, config.algorithm).decode('utf-8')
        return AuthUser(access_token=access_token)
        
      raise GraphQLError('Invalid_Password')
    
  
class CreateStatus(graphene.Mutation):
  class Arguments:
    status_name = graphene.String(required=True)
    
  status = graphene.Field(lambda: StatusType)
  
  @login_required    
  def mutate(self, info, status_name):
    if len(Status.objects.filter(user_id=globals.user))>3:
      raise GraphQLError('Full_Status')
    
    status = Status(
      user_id = globals.user,
      status_name = status_name,
    )
    
    status.save()
    
    return CreateStatus(status=status)
  

class UpdateStatus(graphene.Mutation):
  class Arguments:
    id = graphene.ID(required=True)
    status_name = graphene.String(required=True)
    
  status = graphene.Field(lambda: StatusType)
  
  @login_required
  def mutate(self, info, id, status_name):
    if not Status.objects.filter(user_id=globals.user, id=id):
      raise GraphQLError('Invalid_Status_ID')
    
    status = Status(
      id = id,
      user_id = globals.user,
      status_name = status_name,
    )
    
    status.save()
    
    return UpdateStatus(status=status)
    
      
class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  auth_user = AuthUser.Field()
  create_status = CreateStatus.Field()
  update_status = UpdateStatus.Field()
