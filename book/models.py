from django.db import models

# Create your models here.

class Book(models.Model):
    """
    書本資訊 
    """
    STATUS_CHOICES = [
        ('available', '可借閱'),
        ('borrowed', '已借出'),
        ('maintenance', '維護中'),
    ]

    title=models.CharField(max_length=50,verbose_name="書名")
    author=models.CharField(max_length=20,verbose_name="作者")
    isbn=models.CharField(max_length=13,verbose_name="國際標準書號")
    publication_date=models.DateField(verbose_name="出版日期")
    status=models.CharField(
        max_length=20,choices=STATUS_CHOICES,
                            default="available",verbose_name="借閱狀態")
    
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="創建時間")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="更新時間")
    
    class Meta:
        ordering=['-created_at']
        
    def __str__(self):
        return f"{self.title}-{self.author}"
    