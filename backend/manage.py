#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
from os.path import join, dirname
from dotenv import load_dotenv


def main():
    env_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
