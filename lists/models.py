from django.db import models
from django.urls import reverse

class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    def create_new():
        pass
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['list', 'text'], name='unique_item_list'),
        ]

    def __str__(self):
        return self.text
