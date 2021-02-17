# import bcrypt
# import jwt
# import config

# from graphene_django.utils.testing import GraphQLTestCase
# from graphene.test import Client
# from user.models import User
# from .models import Status, ToDo

# class ToDoTestCase(GraphQLTestCase):  
#   def setUp(self):
#     User(
#       account = "1234",
#       password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
#     ).save()
    
#     Status(
#       user_id = User.objects.get(id=1).id,
#       status_name = "Done"
#     ).save()
    
#     ToDo(
#       status_id = Status.objects.get(id=1).id,
#       title = "Todo",
#       content = "sleep"
#     ).save()
    
#     self.fake_token = jwt.encode({'user_id' : User.objects.get(id=1).id}, config.SECRET_KEY, config.algorithm).decode('utf-8')
  
#   def tearDown(self):
#     User.objects.all().delete()
#     Status.objects.all().delete()
#     ToDo.objects.all().delete()
  
#   # def test_create_status(self):
    
#   #   response = self.query(
#   #     '''
#   #     mutation{
#   #       createStatus(input: $input){
#   #         status{
#   #           statusName
#   #           user{
#   #             id
#   #           }
#   #         }
#   #       }
#   #     }
#   #     ''',
#   #     input_data={'user_id' : 1, 'status_name' : 'In progress'}
#   #   )
    
#   #   self.assertResponseNoErrors(response)