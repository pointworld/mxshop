from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是 get 失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            # django 的后台中密码加密：所以不能 password==password
            # UserProfile 继承的 AbstractUser 中有 def check_password(self, raw_password)
            if user.check_password(password):
                return user
        except Exception as e:
            return None
