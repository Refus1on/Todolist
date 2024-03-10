from django.contrib import admin

from goals.models import GoalCategory, Goals, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')
    readonly_fields = ['created', 'updated']
    list_display_links = ('title',)


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'priority')
    search_fields = ('title', 'description')
    readonly_fields = ['created', 'updated']
    list_display_links = ('title',)


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text')
    search_fields = ('text',)
    readonly_fields = ['created', 'updated']
    list_display_links = ('text',)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goals, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
