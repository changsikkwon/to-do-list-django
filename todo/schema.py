from graphene_django.types import DjangoObjectType, ObjectType
from graphql import GraphQLError
from django_globals import globals
from .models import Status, ToDo
from user.utils import login_required

import graphene


class StatusType(DjangoObjectType):
  class Meta:
    model = Status
    
    
class TodoType(DjangoObjectType):
  class Meta:
    model = ToDo
    

class Query(ObjectType):
  all_status = graphene.List(StatusType)
  all_todo = graphene.List(TodoType)
  todo = graphene.Field(TodoType, id=graphene.ID(required=True))
  
  @login_required
  def resolve_all_status(self, info):
    return Status.objects.filter(user_id=globals.user)
  
  @login_required
  def resolve_all_todo(self, info):
    return ToDo.objects.select_related('status__user').filter(status__user_id=globals.user)
  
  @login_required
  def resolve_todo(self, info, id):
    return  ToDo.objects.select_related('status__user').filter(status__user_id=globals.user).get(id=id)
    
    
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
    if not Status.objects.filter(id=id, user_id=globals.user):
      raise GraphQLError('Invalid_Status_ID')
    
    status = Status(
      id = id,
      user_id = globals.user,
      status_name = status_name,
    )
    
    status.save()
    
    return UpdateStatus(status=status)
  

class DeleteStatus(graphene.Mutation):
  class Arguments:
    id = graphene.ID(required=True)
    
  status = graphene.Field(graphene.String)
  
  @login_required
  def mutate(self, info ,id):
    if Status.objects.filter(user_id=globals.user, id=id):
      raise GraphQLError('Invalid_Status_ID')
    
    status = Status.objects.get(user_id=globals.user, id=id)
    
    status.delete()
    
    return DeleteStatus()
  

class CreateToDo(graphene.Mutation):
  class Arguments:
    status_id = graphene.ID(required=True)
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    
  todo = graphene.Field(lambda: TodoType)
    
  @login_required
  def mutate(self, info, status_id, title, content):
    if Status.objects.filter(id=status_id, user_id=globals.user):
      
      todo = ToDo(
        status_id = status_id,
        title = title,
        content = content,
      )
      
      todo.save()
      
      return CreateToDo(todo=todo)
    
    else:
      raise GraphQLError('Invalid_Status')
    
    
class UpdateToDo(graphene.Mutation):
  class Arguments:
    id = graphene.ID(required=True)
    status_id = graphene.ID(required=True)
    title = graphene.String()
    content = graphene.String()
    
  todo = graphene.Field(lambda: TodoType)
  
  @login_required
  def mutate(self, info, **kwargs):
    if Status.objects.filter(id=kwargs['status_id'], user_id=globals.user):
      
      todo = ToDo.objects.get(id=kwargs['id'], status_id=kwargs['status_id'])
      
      for key, value in kwargs.items():
        setattr(todo, key, value)
        
      todo.save()
      
      return CreateToDo(todo=todo)
    
    else:
      raise GraphQLError('Invalid_Status')
    
    
class DeleteToDo(graphene.Mutation):
  class Arguments:
    id = graphene.ID(required=True)
    
  todo = graphene.Field(graphene.String)
  
  @login_required
  def mutate(self, info ,id):    
    todo = ToDo.objects.get(id=id)
    status_id = todo.status_id
    
    if Status.objects.filter(id=status_id, user_id=globals.user):
      
      todo.delete()
      
      return DeleteToDo()
    
    else:
      raise GraphQLError('Invalid_Status')
    
      
class Mutation(graphene.ObjectType):
  create_status = CreateStatus.Field()
  update_status = UpdateStatus.Field()
  delete_status = DeleteStatus.Field()
  create_todo = CreateToDo.Field()
  update_todo = UpdateToDo.Field()
  delete_todo = DeleteToDo.Field()