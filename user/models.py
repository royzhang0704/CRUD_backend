from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """用戶資訊"""
    # 只寫出要修改的欄位 內建有 
    # username, email, password, is_staff, 
    # is_superuser first_name, last_name, date_joined, is_active, 
    # last_login, groups, user_permissions
    username = models.CharField(
        max_length=64,  # 這裡改成64，默認是150
        verbose_name="用戶名",
        unique=True
    )
    email = models.EmailField(
        verbose_name="電子郵件",
        unique=True  # 添加唯一性約束，默認是可以重複的
    )