import graphene
from to_do_list.schema import Query as to_do_list_query, Mutation as to_do_list_mutation
from user.schema import Query as user_query, Mutation as user_mutation

class Query(to_do_list_query, user_query):
  pass


class Mutation(to_do_list_mutation, user_mutation):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)