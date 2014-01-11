#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    try:
        import etherkeeper.settings_local
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etherkeeper.settings_local")
    except:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etherkeeper.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
