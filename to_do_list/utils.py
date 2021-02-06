from functools import wraps
from graphql import GraphQLError
from django_globals import globals

from .models import User

import jwt
import config


def login_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
      access_token = request.context.META.get('HTTP_AUTHORIZATION')
      
      if access_token is not None:
        try:
          payload = jwt.decode(access_token, config.SECRET_KEY, algorithm = config.algorithm)

        except jwt.InvalidTokenError:
          payload = None
          
        if payload is None:
          raise GraphQLError('Invalid_Token')
        
        user = User.objects.get(id=payload['user_id'])
        globals.user = user.id
        
      else:
        raise GraphQLError('Invalid_Token')

      return func(self, request, *args, **kwargs)
    return wrapper