
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Note



@register(Note)
class NoteIndex(AlgoliaIndex): 
    fields = [
        'title',
        'content', 
    ]