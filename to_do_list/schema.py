import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import User, Status, ToDo

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