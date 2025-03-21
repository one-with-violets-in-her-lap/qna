import os

from dotenv import load_dotenv
import waitress

from flask_app import create_flask_app
from logging_setup import root_logger


load_dotenv()

app = create_flask_app()

root_logger.info("Launching Flask app")

if os.environ.get("MODE") == "DEV":
    app.run(port=8000)
else:
    print("running in production mode with waitress server")
    waitress.serve(app, port=8000)
