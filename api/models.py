from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def total_comment(self):
        return self.comments.count()
    
    def __str__(self):
        return f"{self.title} ({self.user})"

    
    
class Comment(models.Model):
    note = models.ForeignKey('Note', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    # def __str__(self):
    #     return f"Comment by {self.user.username} on {self.note.title}"
    def __str__(self):
        return str(self.user)

    
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = ("user", "note")
        

class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentlikes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)

    