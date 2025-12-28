from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'is_user', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def short_text(self, obj):
        return obj.text[:50]

    short_text.short_description = 'Text'