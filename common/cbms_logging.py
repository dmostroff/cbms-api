import os
import sys
from pathlib import Path
import logging
import logging.config

DEFAULT_LOGFILE='logfile.log'

def get_logging_filename( filename:str = None) -> str:
    fp = Path( os.getenv('LOGGING_FILE') if filename is None else filename)
    if fp.is_file():
        return str(fp)
    if not Path( Path(filename).parent.is_dir()):
        default_logpath = Path.joinpath( Path(__file__).parent.parent, 'log')
        log_path = os.getenv('log_path', default_logpath)
        Path(log_path).mkdir(parents=True, exist_ok=True)
    basename = fp.parts[-1] if len(fp.parts) > 0 else DEFAULT_LOGFILE
    return str(Path.joinpath(Path(log_path), basename))

def set_logging_file( log_filename):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=log_filename, mode='a', encoding='utf-8', delay=False)
    # fh = logging.FileHandler( log_filename, mode='a', encoding='utf-8', delay=False)
    # logging.getLogger().addHandler(fh)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    return

def get_logger( logger_state):
    logger_state = 'prod' if logger_state is None else logger_state
    return logging.getLogger( logger_state)

def setup( logger_state = None):
    yaml_file = Path.joinpath(Path(__file__).parent, 'cbms_log_config.yaml')
    print( yaml_file)
    if yaml_file.is_file():
        import yaml
        with open(yaml_file, 'r') as f:
            try:
                log_cfg = yaml.safe_load(f.read())
                logging.config.dictConfig(log_cfg)
                
            except Exception as e:
                print(str(e))
                print('Error with log file, using default logging')
                set_logging_file(get_logging_filename( ))

    else:
        logging.basicConfig(level=logging.DEBUG)
        print('Config file not found, using Default logging')

    # set_logging_file( filename)
    return get_logger( logger_state)
