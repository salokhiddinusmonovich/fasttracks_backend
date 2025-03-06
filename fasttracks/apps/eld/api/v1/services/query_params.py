from drf_yasg import openapi

def get_token():
    return [openapi.Parameter('token', openapi.IN_QUERY, description="register api token", 
                              type=openapi.TYPE_STRING)
                              ]



