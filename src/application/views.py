"""
views.py

URL route handlers

Note that any handler params must match the URL route params.

"""


from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

from models import PostModel
from decorators import login_required
from forms import PostForm

#URL routing is not here; see urls.py instead

def home():
    return render_template('index.html', home=home)


def blog():
    blog = PostModel.all()
    return render_template('blog.html', blog=blog)


def contact():
    return render_template('contact.html', contact=contact)


@login_required
def admin_only():
    """This view requires an admin account"""
    return render_template('admin_only.html', admin_only=admin_only)


@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = PostModel(
                    title = form.title.data,
                    prose = form.prose.data,
                    author = users.get_current_user()
                    )
        try:
            post.put()
            flash(u'Post successfully saved.', 'success')
            return redirect(url_for('blog'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'failure')
            return redirect(url_for('blog'))
    return render_template('new_post.html', form=form)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

