"""
***********************

You are looking at main.py, the primary Google App Engine (GAE) handler for Canteen.

Are you trying to define page views?  Go to views.py.

Need to fix routing of URLS?  Go to urls.py.

Want to enter additional info, like a date, into a form field?  Set up or adjust database entities in models.py first.

Forms which post to the database are set up in forms.py.  WTFforms is in /packages/flaskext folder.

The database can be manipulated directly via SQL queries in the GAE control panel for this application.

Did you change something and it broke?  Make sure login or admin functions for the above jive with decorators.py.

Make sure you import the necessary module to execute new code on whichever page you changed.

Primary template for HTML pages is base.html; the blog page uses blog_layout.html.

There are two admin pages: the "admin_only" page, and the "new_post" page.  They use the admin_dashboards_layout.html template.

The homepage is index.html.  It's in the templates folder.

***********************

TO DO: 

Fix blog posts to render HTML tags.

***********************

"""

import sys, os

package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)

# Allow unzipped packages to be imported
# from packages folder
sys.path.insert(0, package_dir_path)

# Append zip archives to path for zipimport
for filename in os.listdir(package_dir_path):
    if filename.endswith((".zip", ".egg")):
        sys.path.insert(0, "%s/%s" % (package_dir_path, filename))

from wsgiref.handlers import CGIHandler

from application.settings import DEBUG_MODE
from application import app


def main():
    if DEBUG_MODE:
        # Run debugged app
        from werkzeug_debugger_appengine import get_debugged_app
        app.debug=True
        debugged_app = get_debugged_app(app)
        CGIHandler().run(debugged_app)
    else:
        # Run production app
        from google.appengine.ext.webapp.util import run_wsgi_app
        run_wsgi_app(app)


# Use App Engine app caching
if __name__ == "__main__":
    main()

