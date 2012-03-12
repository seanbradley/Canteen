"""
Initialize Flask app

To compile .scss files using Compass, uncomment line 9 and line 14 
(only for DEBUG mode in development; not for production deployment)

"""

from flask import Flask
from flaskext.gae_mini_profiler import GAEMiniProfiler
#from flaskext.compass import Compass

app = Flask('application')
app.config.from_object('application.settings')
GAEMiniProfiler(app)
#compass = Compass(app)

import urls
