from fastapi import FastAPI, Response

from app.api.v1 import user_router

main_app = FastAPI()

main_app.include_router(user_router, prefix='/api/v1', tags=['user'])
# print(main_app.routes)
# print('ABSHGA')

@main_app.get('/health')
def check_server_status():

    return Response(status_code=200)