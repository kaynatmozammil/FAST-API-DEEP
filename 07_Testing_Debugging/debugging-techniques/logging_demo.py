import logging
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format = "[%(asctime)s](line %(lineno)d) - %(levelname)s - %(message)s",
    datefmt = "%m-%d-%Y %H:%M:%S"
)

@app.get('/debug')
def debug_route():
    print('Inside the route handler.')
    logging.info('Debug endpoint hit')
    logging.info('Another logging info')
    return {'message':'Check logs'}