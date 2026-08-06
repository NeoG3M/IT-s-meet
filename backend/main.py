from fastapi import FastAPI, Response

from json import JSONEncoder

main_app = FastAPI()

@main_app.get('/health')
def check_server_status():

    return Response(status_code=200)