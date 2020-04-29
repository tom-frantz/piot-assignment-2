from flask import Flask

app = Flask(__name__)

# Import of route modules must come after the application object is created
import master.home
import master.register
import master.auth
import master.logout
