import os

# from pathlib import Path

import create_app as ca
import common.settings as settings
import common.db_layer as db
import router
import common.cbms_logging as clog

isApache = "APACHE_RUN_DIR" in os.environ.keys()

# ROOT_DIR = Path(__file__).parent.resolve()

# sys.path.insert(0, ROOT_DIR)
# sys.path.append( ROOT_DIR)
# sys.path.extend( [ROOT_DIR.joinpath(subdir) for subdir in ['admin', 'common', 'database', 'resources', 'models', 'summary', 'clients', 'creditcards']])


settings.load_env()
# logfile = os.getenv('LOGGING_FILE')
clog.setup(os.getenv("ENVIRONMENT", "dev"))


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


db.get_connection()
app = ca.create_app()
app.logger.info("----- Begin -----")

#
try:
    with app.app_context():
        router.before_and_after_requests(app)
        router.set_routes(app)
except Exception as ex:
    app.logger.error(repr(ex))

if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
    # debug=True, use_reloader=False
