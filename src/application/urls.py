"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# Blog
app.add_url_rule('/blog', 'blog', view_func=views.blog)

# Contact page
app.add_url_rule('/contact', 'contact', view_func=views.contact)

# Admin
app.add_url_rule('/admin_only', 'admin_only', view_func=views.admin_only)

# Blog new posts page
app.add_url_rule('/blog/new', 'new_post', view_func=views.new_post, methods=['GET', 'POST'])


## Error handlers

# Handle 403 errors
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

