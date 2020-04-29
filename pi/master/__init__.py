from flask import Flask

app = Flask(__name__)

# import of route modules must come after the application instance
import master.home
import master.register
import master.auth
import master.logout
