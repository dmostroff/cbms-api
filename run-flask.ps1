echo $PSScriptRoot
$env:FLASK_APP="__init__.py"
# $env:FLASK_ENV="development"
$env:FLASK_DEBUG=1
$env:FLASK_RUN_PORT=5000
$env:FLASK_RUN_HOST="cbmsapi.com"
# . $PSScriptRoot\venv\Scripts\activate
# . "$PSScriptRoot\venv\Scripts\flask run"

