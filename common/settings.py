# settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

def load_env():
    dotenv_path = Path.joinpath(Path(__file__).parent.parent, '.env')
    load_dotenv(dotenv_path)
    # OR, the same with increased verbosity
    # load_dotenv(verbose=True)

    print( "settings")
    print( 'dotenv_path', dotenv_path)
    print( 'CONNECTION_STRING', os.getenv('CONNECTION_STRING'))
    print( 'API_VERSION', os.getenv('API_VERSION'))
    print( 'LOGGING_FILE', os.getenv('LOGGING_FILE'))
    print( "end settings")
