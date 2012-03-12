===================================================
CANTEEN: a version of Flask ready for mobile combat
===================================================

Flask + Compass + Bootstrap.  I call the result Canteen.  :)

Canteen is a simple hack built on Flask--a Python-based "microframework", coupled with .scss files compiled via the Flask-Compass extension.  Compass is a Ruby-based CSS authoring framework. The styling of Canteen itself is mainly stolen from Bootstrap, a responsive HTML5 framework suitable for mobile web apps by the folks from Twitter.

This is the first version of this app, so please be forgiving if it's buggy.  The .scss files should be DRYed out more, and presentational class names can be better compartmentalized away from the markup.  The stylesheets contain a lot of unused stuff--purposefully--for easy future extensibility from a design standpoint. Presently, however, the .scss and resultant .css files are relatively ginormous, and ought to be minified for use in a production environment. When you're ready to rock-n-roll for any consumer-facing site, I recommend serving up the static files via a CDN, like AWS Cloudfront.

************************************

INSTALL THE APP (THE EASY WAY)
==============================

These instructions assume you've already set up a Google App Engine (GAE) account and have installed the GAE launcher on your local machine.  It also assumes you've chosen and selected a new application name via the GAE administrative dashboard, which you can find at this link:

NOTE: Your app.yaml's application name must not be an application name already reserved on Google App Engine. 

Then, make sure Python is installed on your machine.  Python 2.7 is recommended.  If you have difficulty getting your app to play nice with GAE, try the last stable release of Python 2.5.

NOTE: the Flask docs recommend running the app in a virtual environment, even for a production server.  More about that here::

	http://flask.pocoo.org/docs/installation/#virtualenv

Canteen--that is, this particular customization of Flask--is designed to run on Google App Engine (GAE), so don't worry about setting up a virtual env if you intend to tweak it and run it from within the GAE Launcher or via the GAE command line tools.  However, if you intend to work on the app directly via the command line--without using GAE's CLI tools--or if you intend to install the app on AWS, then, yes, please do your dev work inside a virtual env.  (In that case, the following instructions regarding the app.yaml file required by GAE will not be of much relevance to you.)

Once you have determined your development environment...

1) Download this package onto your development machine. (If you're reading this, you've probably already did that.)

2) unpack / unzip the package (You probably already did that, too.)

3) Then CD into the Canteen directory and run::

	python setup.py install

4) Navigate to the Canteen directory on your local harddrive.  Inside of that directory, find the src/app.yaml file.  Edit the "application" variable in the app.yaml file.  Presently, it's set as application: seanbradley-1 ...but you need to change it in the text editor of your choice so that it is the same as the name you selected inside of GAE's web-based admnistrative dashboard.  

5) Open up GAE's Launcher, click [File] --> [Add Existing Application] --> find the "Canteen\src" directory on your harddrive --> then, in the Launcher, click [Start].  Make any desired changes and then [Deploy].

NOTE: You may have to adjust URLs in the src\templates\admin_dashboards_layout.html template.
 

************************************

TO RUN THE APP FROM THE COMMAND LINE
===+++==============================

These are instructions for folks who don't want to use Google App Engine, and who know what they're doing when it comes to deploying Flask.  You will have to change the src/application/_init_.py file as well as other files listed in src/main.py.

Assuming you've tweaked the app correctly and have set up your virtual env to run the app outside of GAE, CD to the Canteen directory and enter::

	python runserver.py

Ctrl-C to stop it.

In development mode, line 3 of the runserver.py file should be set to debug=True.  This will run the debugger in your client, and any template changes will be instantly apparent upon a browser refresh. When you're ready to run your site in production mode, change line 3 of the runserver.py file to debug=False, and restart the server.


************************************

INDEX OF IMPORTANT FILES
========================

*app.yaml* and *main.py*  Google App Engine needs these files to run.  In app.yaml, do not use Python27 for the runtime, and do not set threadsafe=true, unless you are deploying to a non-GAE machine.  *main.py* is the primary Google App Engine (GAE) handler for Canteen.

Are you trying to define page views?  Go to views.py.

Need to fix routing of URLS?  Go to urls.py.

Want to enter additional info, like a date, into a form field?  Set up or adjust database entities in models.py first.

Forms which post to the database are set up in forms.py.  WTFforms is in /packages/flaskext folder.

FYI: The database can be manipulated directly via SQL queries in the GAE control panel for this application.

Did you change something and it broke?  Make sure login or admin functions for the above jive with decorators.py.

Make sure you import the necessary module to execute new code on whichever page you changed.

Primary template for HTML pages is base.html; the blog page uses blog_layout.html.

There are two admin pages: the "admin_only" page, and the "new_post" page.  They both require the admin_dashboards_layout.html template.

The homepage is index.html.  It's in the templates folder.

***********************

TO DO: 

Fix blog posts to render HTML tags.  

Enable compiling of altered .scss files in a production environment.


************************************

A WORD ABOUT SASS AND COMPASS
=+++++++=====================

You can learn more about Sass at sass-lang.org. 

Using Compass requires Ruby.

It is not a *hardcore prerequisite* to install Ruby or Compass.  Why?

First and foremost, the app has the Flask-Compass extension.  The _init_.py file is tweaked to incorporate this; it relies on a config.rb file in the /static/compass_project directory.  Even so, if the compilation of .scss files is buggy, you may then want to consider installing Ruby and Compass for development purposes.


Compass-style.org says...

The instructions to integrate Compass/Sass with a Python framework are:

1. Use Compass/Sass
2. Use your Python framework (in this case, Flask)

In other words:

>>>"Compass and Sass are built in Ruby. When the rest of your project is also built in Ruby, it makes sense to squeeze every last ounce of convenient automatic integration, like having your project automatically compile Sass to CSS for you at runtime. But that integration is not actually necessary, and when the rest of your project is not Ruby, you pay a lot more for that little bit of convenience."

Hence, extrapolating that advice to Flask, except for a minor edit to the I've made no attempt to hook in Compass during installation or to compile Sass at runtime.

During development: if you run Python *and* Ruby on your local machine *and* install Compass, you can open up a terminal, fire up Ruby, and ask Compass to watch for changes in your .scss file as you edit it.  Meanwhile, via a separate terminal, you can fire up Python, and run your Flask development server. (That's not such a brilliant idea for a production webserver, of course, as it creates a lot of overhead.)

After revising and compiling your .scss files into .css, you would then upload the new stylesheets to your production server (or S3 if you're using AWS Cloudfront).  

************************************

INSTALLING COMPASS SEPARATELY
=============================

If you intend to compile any adjusted .scss files using Compass...
 

First intall Ruby.  Instructions on how to install Ruby are here::

	http://www.ruby-lang.org/en/downloads/


Once Ruby is installed, you can install Compass like so::

	gem install compass
	
	cd /path/to/Canteen/static/compass_project/

	compass watch


The compass watch process will automatically compile any revised .scss files into the .css files in the stylesheets directory whenever they change. 


************************************

USING PYSCSS INSTEAD OF COMPASS
===============================

Alternatively, you can get around messing with Ruby (or pyRuby or rython, etc.) by your .scss files on your server using pyScss.

pyScss is still in development, but using it allows you to have a purely Pythonic development or production environment.  Check out the pyScss Github repo at::

	https://github.com/Kronuz/pyScss


After installing pyScss, you can compile a .scss file using::

	python -mscss < file.scss


Afterwards, you'll need to move the compiled file into the appropriate Canteen directory--for example, like so::

	mv path/to/your_file.scss /application/static/compass_project/stylesheets


************************************

CONTACT
=======


Feel free to e-mail me and make suggestions or ask questions.  Your input is highly valued::

sean@bravoflix.com


************************************

CREDITS
=======

Flask--a Python microframework--is the work of Armin Ronacher and a couple other folks at:
http://flask.pocoo.org/

Boostrap--a responsive CSS framework--is built by some of the good folks at Twitter:
http://twitter.github.com/bootstrap/

Compass--a stylesheet authoring environment for Sass--was built by Christopher M. Eppstein:
http://compass-style.org/

Canteen on Google App Engine is based in part on Francisco Souza's installation of Flask at:
http://f.souza.cc/2010/08/flying-with-flask-on-google-app-engine/

Canteen borrows heavily from the work of Kamal Gill and his Flask / GAE template, which uses HTML5Boilerplate instead of Bootstrap:
https://github.com/kamalgill/flask-appengine-template


