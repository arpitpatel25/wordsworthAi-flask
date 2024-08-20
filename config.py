# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# class Config:
#     password = os.getenv('MONGODB_ATLAS_USER_PASSWORD')
#     MONGO_URI = ("mongodb+srv://arpit_evaluateAi:"+password+"@evaluateai-dev-cluster.hji44fk.mongodb.net"
#                  "/wordsworthai?retryWrites=true&w=majority")
#
#     S3_BUCKET = 'evaluate.ai-dev-answer-images-bucket'

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    password = os.getenv('MONGODB_ATLAS_USER_PASSWORD')
    MONGO_URI = ("mongodb+srv://arpit_evaluateAi:"+password+"@evaluateai-dev-cluster.hji44fk.mongodb.net"
                 "/wordsworthai?retryWrites=true&w=majority")

    S3_BUCKET = 'evaluate.ai-dev-answer-images-bucket'
    MONGODB_SETTINGS = {
        'db': 'wordsworthai',
        'host': MONGO_URI
    }
