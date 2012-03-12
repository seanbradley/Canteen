"""
See flaskext.compass.Compass or the HTML documentation for details.
"""

import os
import subprocess
import re
import time
import warnings
import errno
from flask import request


CONFIG_LINE_RE = re.compile(ur'^\s*?(\S+)\s*?=\s*(.*)\s*$')


class Compass(object):
    """
    This is a very basic extension for Flask that searches for compass projects
    within an application's directory and compiles it.

    By default this is only done when the application is in debug mode since
    with each request the extension has to check all relevant files to see if
    there even *is* something to compile.
    """

    def __init__(self, app=None):
        self.app = app
        self.configs = {}
        self.log = None
        self.config_files = None
        self.requestcheck_debug_only = None
        self.debug_only = None
        self.skip_mtime_check = None
        self.compass_path = None
        self.disabled = False
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        """
        Initialize the application once the configuration has been loaded
        there.
        """
        self.app = app
        self.log = app.logger.getChild('compass')
        self.log.debug("Initializing compass integration")
        self.compass_path = self.app.config.get('COMPASS_PATH', 'compass')
        self.config_files = self.app.config.get('COMPASS_CONFIGS', None)
        self.requestcheck_debug_only = self.app.config.get(
                'COMPASS_REQUESTCHECK_DEBUG_ONLY', True)
        self.skip_mtime_check = self.app.config.get(
                'COMPASS_SKIP_MTIME_CHECK', False)
        self.debug_only = self.app.config.get(
                'COMPASS_DEBUG_ONLY', False)
        self.disabled = self.app.config.get('COMPASS_DISABLED', False)

        if not self.debug_only:
            self.compile()
        if (not self.debug_only) \
                and (not self.requestcheck_debug_only or self.app.debug):
            self.app.after_request(self.after_request)

    def compile(self):
        """
        Main entry point that compiles all the specified or found compass
        projects.
        """
        if self.disabled:
            return
        self._check_configs()
        for _, cfg in self.configs.iteritems():
            cfg.parse()
            if cfg.changes_found() or self.skip_mtime_check:
                self.log.debug("Changes found for " + cfg.path \
                        + " or checks disabled. Compiling...")
                cfg.compile(self)

    def after_request(self, response):
        """
        after_request handler for compiling the compass projects with
        each request.
        """
        if response is not None and request is not None:
            # When used as response processor, only run if we are requesting
            # anything but a static resource.
            if request.endpoint in [None, "static"]:
                return response
        self.compile()
        return response

    def _check_configs(self):
        """
        Reloads the configuration files.
        """
        configs = set(self._find_configs())
        known_configs = set(self.configs.keys())
        new_configs = configs - known_configs
        for cfg in (known_configs - configs):
            self.log.debug("Compass configuration has been removed: " + cfg)
            del self.configs[cfg]
        for cfg in new_configs:
            self.log.debug("Found new compass configuration: " + cfg)
            self.configs[cfg] = CompassConfig(cfg)

    def _find_configs(self):
        """
        Scans the project directory for config files or returns
        the explicitly specified list of files.
        """
        if self.config_files is not None:
            return self.config_files

        # Walk the whole project tree and look for "config.rb" files
        result = []
        for path, _, files in os.walk(self.app.root_path):
            if "config.rb" in files:
                result.append(os.path.join(path, "config.rb"))
        return result


class CompassConfig(object):
    """
    Abstraction for the config.rb file.
    """

    def __init__(self, path):
        self.path = path
        self.base_dir = os.path.dirname(path)
        self.last_parsed = None
        self.src = None
        self.dest = None

    def parse(self, replace=False):
        """
        Parse the given compass config file
        """
        if self.last_parsed is not None \
                and self.last_parsed > os.path.getmtime(self.path) \
                and not replace:
            return
        self.last_parsed = time.time()
        with open(self.path, 'r') as file_:
            for line in file_:
                match = CONFIG_LINE_RE.match(line.rstrip())
                if match:
                    if match.group(1) == 'sass_dir':
                        self.src = os.path.join(
                                self.base_dir, match.group(2)[1:-1])
                    elif match.group(1) == 'css_dir':
                        self.dest = os.path.join(
                                self.base_dir, match.group(2)[1:-1])

    def changes_found(self):
        """
        Returns True if the target folder is older than the source folder.
        """
        if self.dest is None:
            warnings.warn("dest directory not found!")
        if self.src is None:
            warnings.warn("src directory not found!")
        if self.src is None or self.dest is None:
            return False
        dest_mtime = -1
        src_mtime = os.path.getmtime(self.src)
        if os.path.exists(self.dest):
            dest_mtime = os.path.getmtime(self.dest)
        return src_mtime >= dest_mtime

    def compile(self, compass):
        """
        Calls the compass script specified in the compass extension
        with the paths provided by the config.rb.
        """
        try:
            output = subprocess.check_output(
                    [compass.compass_path, 'compile', '-q'],
                    cwd=self.base_dir)
            os.utime(self.dest, None)
            compass.log.debug(output)
        except OSError, e:
            if e.errno == errno.ENOENT:
                compass.log.error("Compass could not be found in the PATH " +
                    "and/or in the COMPASS_PATH setting! " +
                    "Disabling compilation.")
                compass.disabled = True
            else:
                raise e
