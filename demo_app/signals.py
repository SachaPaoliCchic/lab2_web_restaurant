from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Client
import os

@receiver(post_delete, sender=Client)
def delete_client_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Client)
def replace_client_image(sender, instance, **kwargs):
    if not instance.pk:
        return  
    try:
        old_client = Client.objects.get(pk=instance.pk)
    except Client.DoesNotExist:
        return
    old_image = old_client.image
    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
