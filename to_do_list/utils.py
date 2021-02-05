from functools import wraps
from django.http import JsonResponse
from graphql import GraphQLError

from .models import User

import jwt
import config


def login_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
          try:
            payload = jwt.decode(access_token, config.SECRET_KEY, algorithm = config.algorithm)
  
          except jwt.InvalidTokenError:
            payload = None
            
          if payload is None:
            raise GraphQLError('Invalid_Token')
            
          user = User.objects.get(id=payload['id'])
          request.user = user
          
        else:
          raise GraphQLError('Invalid_Token')

        return func(self, request, *args, **kwargs)
    return wrapper