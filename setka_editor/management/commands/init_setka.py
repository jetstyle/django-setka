import os
import re

from django.core.management.base import BaseCommand

from setka_editor.utils.editor import update_setka_build


class Command(BaseCommand):
    help = 'First setka initialization. Getting required files'

    def handle(self, *args, **options):
        update_setka_build()
        self.stdout.write(self.style.SUCCESS('Success!'))
