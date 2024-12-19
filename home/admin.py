from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['title','author','status','publication_date']
    list_filter=['status']
    search_fields=['title','status']
    # Register your models here.