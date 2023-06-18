"""
Settings for mainapp
"""
from django.apps import AppConfig
from django.conf import settings
from django.core import management


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapps.mainapp'

    def ready(self):
        """
        Initialize mainapp.

        !!!IMPORTANT!!!: This process runs only once when you use manage.py (runserver, migration etc.).
        Import models inside this function.
        Mainly used to initialize DB constants.

        :param (No param)
        :return: (No return)
        """
        # Initialize DB constants
        # (See comment in mainapp > constants > const.py)
        # Skip updating db_const.py by db data when this method is called by create_fixture_file_from_db_const.py,
        # the opposite process.
        if not settings.IS_FIXTURE:
            management.call_command('create_db_const_file')
