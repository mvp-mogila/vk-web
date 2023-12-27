from django.core.management.base import BaseCommand

from app.services import cache_popular_tags

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def handle(self, *args, **kwargs):
        cache_popular_tags()
        with open("/home/artem/Desktop/tmp.txt", "a") as file:
            file.write('Hello from python')