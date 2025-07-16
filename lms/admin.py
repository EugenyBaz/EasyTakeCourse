from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "preview",
        "description",
    )
    ordering = ("id",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "name",
        "preview",
        "description",
        "link",
    )
    ordering = ("id",)
