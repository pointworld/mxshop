from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# post_save: 接收信号的方式
# sender: 接收信号的 model
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为 update 的时候也会进行 post_save
    if created:
        password = instance.password
        # instance 相当于 user
        instance.set_password(password)
        instance.save()
