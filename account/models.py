from django.db import models
from django.conf import settings


# Create your models here.
class UserFollows(models.Model):
    objects = None
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by')
    username = models.CharField(max_length=150, blank=True)
    
    class Meta:
        unique_together = ('user', 'followed_user', )

    def __str__(self):
        return "Abonnement:" + str(self.user) + "Abonnés:" + str(self.followed_user)
