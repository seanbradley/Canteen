"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators


class PostForm(wtf.Form):
    title = wtf.TextField('Title: something buzz-worthy...', validators=[validators.Required()])
    prose = wtf.TextAreaField('Content: something beautiful...', validators=[validators.Required()])



