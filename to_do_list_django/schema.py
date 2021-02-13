import graphene
from user.schema import Query as user_query, Mutation as user_mutation
from todo.schema import Query as todo_query, Mutation as todo_mutation

class Query(user_query, todo_query):
  pass


class Mutation(user_mutation, todo_mutation):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)