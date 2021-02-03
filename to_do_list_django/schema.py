import graphene
from to_do_list.schema import Query as to_do_list_query, Mutation as to_do_list_mutation

class Query(to_do_list_query):
  pass


class Mutation(to_do_list_mutation):
  pass

schema = graphene.Schema(query=Query, mutation=Mutation)