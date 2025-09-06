from django.apps import AppConfig

class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # def ready(self):
    #     from algoliasearch_django import AlgoliaIndex
    #     from algoliasearch_django.decorators import register
    #     from .models import Note
    #     from accounts.models import Profile

    #     @register(Note)
    #     class NoteIndex(AlgoliaIndex):
    #         fields = ('id', 'content', 'created_at')
    #         settings = {'searchableAttributes': ['content']}
            
    #         def get_birth_date(self, obj):
    #             return obj.birth_date.isoformat() if obj.birth_date else None

    #     @register(Profile)
    #     class ProfileIndex(AlgoliaIndex):
    #         fields = ('id', 'bio')  # Profile probably doesn’t have "content"
    #         settings = {'searchableAttributes': ['user__username', 'bio']}
            
    #         def get_birth_date(self, obj):
    #             return obj.birth_date.isoformat() if obj.birth_date else None
