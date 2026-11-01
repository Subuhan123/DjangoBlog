from django.contrib import admin
from .models import Club, Activity, Signup, CourseNote


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0
    fields = ('title', 'start_time', 'location', 'status')


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'founded_date', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    inlines = [ActivityInline]


class SignupInline(admin.TabularInline):
    model = Signup
    extra = 0
    fields = ('user', 'status', 'remark', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'start_time', 'location',
                    'capacity', 'approved_count', 'status')
    list_filter = ('status', 'club')
    search_fields = ('title', 'location')
    date_hierarchy = 'start_time'
    inlines = [SignupInline]


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'activity__title')


@admin.register(CourseNote)
class CourseNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'author', 'is_public', 'updated_at')
    list_filter = ('course', 'is_public')
    search_fields = ('title', 'course')
