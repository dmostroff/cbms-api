import os
from flask import Flask
from flask_cors import CORS
import admin.user_login_service as uls

def create_app():
    app = Flask(__name__)
    app.config.update( 
        CORS_HEADERS = 'Content-Type',
        DEBUG = True,
        SERVERNAME=os.getenv( "SERVERNAME", "cbmsapi.com:8080"),
        use_debugger=True,
        use_reloader=False,
        passthrough_errors=True
    )
    CORS(app, 
        resources=r'/*',
        supports_credentials=True, 
        expose_headers=uls.AUTHORIZATION
        )

    return app

