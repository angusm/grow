"""RC Config control class."""

import datetime
import os
import time
import yaml
from grow.common import base_config


RC_FILE_NAME = '.growrc.yaml'
RC_LAST_CHECKED_DELTA = datetime.timedelta(hours=1)


class RCConfig(base_config.BaseConfig):
    """Config for Grow RC file."""

    def __init__(self, config=None, internal_time=time.time):
        super(RCConfig, self).__init__(config=config)
        self._time = internal_time
        if config is None:
            self.read()

    @staticmethod
    def _is_ci_env():
        if 'CI' in os.environ:
            return True
        return False

    @property
    def filename(self):
        """Filename of the RC File."""
        return os.path.expanduser('~/{}'.format(RC_FILE_NAME))

    @property
    def last_checked(self):
        """Timestamp of the last time checked for sdk update."""
        return self.get('update.last_checked', 0)

    @last_checked.setter
    def last_checked(self, value):
        """Timestamp of the last time checked for sdk update."""
        return self.set('update.last_checked', value)

    @property
    def needs_update_check(self):
        """Check if the update check needs to be done."""
        if self._is_ci_env():
            return False
        time_passed = self._time() - self.last_checked
        return time_passed > RC_LAST_CHECKED_DELTA.total_seconds()

    def read(self):
        """Reads the RC config from the system."""
        rc_file_name = self.filename
        if not os.path.isfile(rc_file_name):
            self._config = {}
            return
        with open(rc_file_name, 'r') as conf:
            self._config = yaml.load(conf.read())

    def reset_update_check(self):
        """Reset the timestamp of the last_checked."""
        self.last_checked = self._time()

    def write(self):
        """Writes the RC config to the system."""
        rc_file_name = self.filename
        with open(rc_file_name, 'w') as conf:
            conf.write(yaml.safe_dump(self._config, default_flow_style=False))
