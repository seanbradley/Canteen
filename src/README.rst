==========================================
CANTEEN: Flask outfitted for mobile combat
==========================================

Flask + Compass + Bootstrap.  I call the result Canteen.  :)

Canteen is a built on Flask--a Python-based "microframework"--coupled with .scss files compiled with Compass.  (While the Flask-Compass extension is integrated into this Python app for development use, Compass itself is a Ruby-based stylesheet authoring environment for Sass.)

In addition, the front-end of Canteen is inspired by Bootstrap, a wonderfully responsive HTML5 framework suitable for mobile web apps.  To see what that styling looks like, visit www.seanbradley.biz.  There you'll see the app served up from Google App Engine (GAE). Resizing your browser will give you a taste for how the app might display on any number of mobile devices.

Perhaps the biggest inspiration for Canteen is Kamal Gill's version of Flask on GAE, which uses HTML5Boilerplate instead of Bootstrap, as well as Fransico Souza's code snippets for deploying Flask on GAE.  In its essence, Canteen was built from clones of, and a lot of tweaks to, those two sources of code.

Canteen is still in bootcamp.  This is the first version of this app, so please be forgiving if it's not as fit as it ought to be.  The .scss and .css files could probably be DRYed out more, and presentational class names could be more effectively squared away when it comes to the markup.  The stylesheets need trimming before deployment to a production environment...  For this version, I've purposefully left extra code in the base stylesheet, as a strategy for future experimentation and ready extensibility from a design standpoint. Tighten-up and minify the stylesheets for use in a production environment. When you're ready to rock-n-roll and deploy the app on any consumer-facing site, I recommend not only nixing any unnecssary style-related code, and even the .scss files, but also serving up all static files via a CDN, like AWS Cloudfront.

************************************

INSTALL THE APP (THE EASY WAY)
==============================

These instructions assume you already have a Google App Engine account (also known as GAE)* and have installed the GAE launcher on your local machine.  It also assumes you've chosen and selected a new application name via the GAE administrative dashboard.  If not, you can get started with GAE at:

	http://appengine.google.com


NOTE: GAE will ask you to give your application a name.  That name will be synonymous with the application name inside Canteen's app.yaml file.  The name you choose for your version of Canteen must not be synonymous with another application already reserved on Google App Engine. 


Of course, make sure, too, that Python is installed on your local machine.  Python 2.7 is recommended.  If you have difficulty getting your app to play nice with GAE, try using the last stable release of Python 2.5.


NOTE: the Flask docs recommend running the app in a virtual environment, even for a production server.  More about that here::

	http://flask.pocoo.org/docs/installation/#virtualenv


Because Canteen is designed to run on GAE, and, hence, is most easily tested and developed via the GAE Launcher utility, don't worry about setting up a virtual env UNLESS you want to hammer away on it via the command line.  If you choose to develop Canteen via the command line--without using GAE's CLI tools--OR if you intend to install the app on AWS, then, yes, *please* do your dev work inside a virtual env.  (In that case, the following instructions regarding the app.yaml file required by GAE will not be of much relevance to you.)

Once you have determined your development environment...

1) Pull this repo onto your development machine. (If you're reading this, you've probably already did that.)

2) unpack / unzip the package (You probably already did that, too.)

3) Then CD into the Canteen directory and run::

	python setup.py install

4) Inside of the Canteen directory, you'll find the src/app.yaml file.  Edit the application name and version in the app.yaml file.  Presently, it's set as application: seanbradley-2 and version: 3  ...but you need to change name in the text editor of your choice so that it is the same as the name you selected inside of GAE's web-based admnistrative dashboard.  Change the version number to 1.

5) Open up GAE's Launcher, click [File] --> [Add Existing Application] --> find the "Canteen\src" directory on your harddrive --> then, in the Launcher, click [Start].  Make any desired changes and then [Deploy].


You'll be in the trenches and behind the wire before you know it.


NOTE: You may also have to adjust URLs in the src\templates\admin_dashboards_layout.html template.

************************************

TO RUN THE APP FROM THE COMMAND LINE
===+++==============================

These are instructions for folks who don't want to use Google App Engine, and who know what they're doing when it comes to deploying Flask.  You will have to change the src/application/_init_.py file as well as other files listed in the comments of the src/main.py file.

Assuming you've tweaked the app correctly and have set up your virtual env to run the app outside of GAE, CD to the Canteen directory and enter::

	python runserver.py

Ctrl-C to stop it.

When in development mode, line 3 of the runserver.py file should be set to debug=True.  This will run the debugger in your client via the localhost address, and any template changes will be instantly apparent upon a browser refresh.  If you've also installed Compass (and run it from a Ruby command line, OR if you have effectively switched on the Compass-Flask extension (by uncommenting the appropriate line in the app.yaml fileo), then compiling changes to your .scss files and checking the resultant impact on the app's styling is a breeze.  When you're ready to run your site in production mode, change line 3 of the runserver.py file to debug=False.


************************************

INDEX OF IMPORTANT FILES
========================

*app.yaml* and *main.py*  are files that Google App Engine needs to run Canteen.  In app.yaml, do not use Python27 for the runtime, and do not set threadsafe=true (unless you are deploying to a non-GAE machine).  *main.py* is the primary Google App Engine (GAE) handler for the app.

Are you trying to define page views?  Go to views.py.

Need to fix routing of URLS?  Go to urls.py.

Want to enter additional info, like a date, into a form field?  Set up or adjust database entities in models.py first.

Forms which post to the database are set up in forms.py.  WTFforms--the Flask extension which makes integrating forms easier--can be found in the /packages/flaskext directory.

One little plus for using GAE: the database can be manipulated directly via SQL queries in the GAE control panel.

Did you change something for the admin side of the site and it broke?  Make sure login functions for your views jive correctly with decorators.py.

And, of course, make sure you import the necessary module to execute new code on whichever page you changed.

Finally, about the app's templates (which use Jinja)...

The primary template for HTML pages is base.html; however, the blog page uses blog_layout.html. And...

There are two admin pages: the "admin_only" page, and the "new_post" page.  Both of these pages require/extend the admin_dashboards_layout.html template.

The homepage is index.html.  It's in the templates directory.

***********************

TO DO: 

Fix blog posts to render HTML tags.  

Enable compiling of altered .scss files in a production environment(?)


************************************

A WORD ABOUT SASS AND COMPASS
=+++++++=====================

You can learn more about Sass at sass-lang.org. 

Yes, using Compass requires Ruby, but, technically, it's not a *hardcore* prerequisite to install Ruby or Compass.  Why?

First and foremost, the app has the Flask-Compass extension.  It relies on a config.rb file in the /static/compass_project directory.  (Right now, for this version, I cannot guarantee that the config.rb file is totally up-to-date, but it will be soon.) Even so, if the compilation of .scss files is impossibly buggy, you may then want to consider installing Ruby and Compass for development purposes.

But if you're a Pythonista and feel like Ruby is a potential enemy sympathizer, Compass-style.org says...

>>>The instructions to integrate Compass/Sass with a Python framework are:

>>>1. Use Compass/Sass
>>>2. Use your Python framework [in this case, Flask]

In other words:

>>>"Compass and Sass are built in Ruby. When the rest of your project is also built in Ruby, it makes sense to squeeze every last ounce of convenient automatic integration, like having your project automatically compile Sass to CSS for you at runtime. But that integration is not actually necessary, and when the rest of your project is not Ruby, you pay a lot more for that little bit of convenience."

Hence, extrapolating that advice to Canteen, I've made no attempt (yet) to fully hook in Compass during installation or to compile Sass at runtime.  I've only put them close at hand for your convenience.

During development: if you run Python *and* Ruby on your local machine *and* install Compass, you can: 1) fire up a Ruby terminal, and ask Compass to watch for changes to your .scss files and freely edit them.  Meanwhile, you can also open up a separate Python terminal (or GAE Launcher), and run your Flask development server. (This is not, as they say in the service, "high-speed" I know.  If you do it, and someone from the Python community calls you a Pinko, don't come crying to me.)

After revising and compiling your .scss files into .css, you would then upload the new stylesheets to your production server (or deploy a new version of your app to GAE, or upload the revised files to S3 if you're using AWS Cloudfront).  

************************************

INSTALLING COMPASS SEPARATELY
=============================

If you do, in fact, intend to compile any adjusted .scss files using Compass...
 

First intall Ruby.  

Once Ruby is installed, you can install Compass like so::

	gem install compass
	
	cd /path/to/Canteen/static/compass_project/

	compass watch


The compass watch process will automatically compile any revised .scss files into the .css files in the stylesheets directory whenever they change. 


************************************

USING PYSCSS INSTEAD OF COMPASS
===============================

Alternatively, if you're in Python's "Special Operations", you can get around messing with Ruby (or pyRuby or rython, etc.) by compiling your .scss files on your server using *pyScss*.

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

Flask--a Python microframework--is the work of Armin Ronacher and a couple other folks at Pocoo:
http://flask.pocoo.org/

Boostrap--a responsive CSS framework--is built by some of the good folks at Twitter:
http://twitter.github.com/bootstrap/

Compass--a stylesheet authoring environment for Sass--was built by Christopher M. Eppstein:
http://compass-style.org/

Canteen on Google App Engine is based in part on Francisco Souza's installation of Flask at:
http://f.souza.cc/2010/08/flying-with-flask-on-google-app-engine/

Canteen borrows heavily from the work of Kamal Gill and his Flask / GAE template, which uses HTML5Boilerplate instead of Bootstrap:
https://github.com/kamalgill/flask-appengine-template

*NB: I am not an unbridled fan of GAE, but it's especially handy if your free tier at AWS has been exhausted. ;-)

