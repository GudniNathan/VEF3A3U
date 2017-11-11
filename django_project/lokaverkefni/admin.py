from django.contrib import admin
from .models import *

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'mysql'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)


# Register your models here.
admin.site.register(Courses, MultiDBModelAdmin)
admin.site.register(Divisions, MultiDBModelAdmin)
admin.site.register(Restrictors, MultiDBModelAdmin)
admin.site.register(Schools, MultiDBModelAdmin)
admin.site.register(Semesters, MultiDBModelAdmin)
admin.site.register(Studentcourses, MultiDBModelAdmin)
admin.site.register(Students, MultiDBModelAdmin)
admin.site.register(Trackcourses, MultiDBModelAdmin)
admin.site.register(Tracks, MultiDBModelAdmin)