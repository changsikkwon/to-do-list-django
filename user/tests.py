import bcrypt

from graphene_django.utils.testing import GraphQLTestCase
from .models import User

class ToDoTestCase(GraphQLTestCase):  
  def setUp(self):
    User(
      account = "1234",
      password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    ).save()
  
  def tearDown(self):
    User.objects.all().delete()
  
  def test_create_user(self):
    response = self.query(
      '''
      mutation{
        createUser(account:"123", password:"1234"){
          user{
            account
            password
          }
        }
      }
      '''
    )
      
    self.assertResponseNoErrors(response)

  def test_auth_user(self):
    response = self.query(
      '''
      mutation{
        authUser(account:"1234", password:"1234"){
          accessToken
        }
      }
      '''
    )
    
    self.assertResponseNoErrors(response)