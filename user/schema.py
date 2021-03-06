import graphene
import bcrypt
import jwt
import config

from graphene_django.types import DjangoObjectType, ObjectType
from graphql import GraphQLError
from .models import User

class UserType(DjangoObjectType):
  class Meta:
    model = User
    
    
class Query(ObjectType):
  pass
    
    
class CreateUser(graphene.Mutation):
  class Arguments:
    account = graphene.String(required=True)
    password = graphene.String(required=True)
    
  user = graphene.Field(lambda: UserType)
  
  def mutate(self, info, account, password):
    if User.objects.filter(account=account).exists():
      raise GraphQLError('Already_Exist_Account')
    if len(account) < 4:
      raise GraphQLError('Short_Account')
    if len(password) < 8:
      raise GraphQLError('Short_Password')
    
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

    
    
class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  auth_user = AuthUser.Field()