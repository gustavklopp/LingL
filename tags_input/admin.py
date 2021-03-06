from django.contrib import admin

from . import fields
from . import widgets


class TagsInputMixin(object):

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        '''
        Get a form Field for a ManyToManyField.
        '''
        # If it uses an intermediary model that isn't auto created, don't show
        # a field in admin.
        if not db_field.rel.through._meta.auto_created:
            return None

        queryset = db_field.rel.to._default_manager.get_queryset()

        kwargs['queryset'] = queryset
        kwargs['widget'] = widgets.AdminTagsInputWidget(
            verbose_name=db_field.verbose_name,
            is_stacked=db_field.name in self.filter_vertical,
            attrs=kwargs.get('attrs'),
            choices=kwargs.get('choices', ()),
        )
        kwargs['required'] = not db_field.blank
        kwargs['help_text'] = getattr(db_field, 'help_text', None)
        kwargs['verbose_name'] = getattr(db_field, 'verbose_name', None)

        # Ugly hack to stop the Django admin from adding the + icon
        if db_field.name not in self.raw_id_fields:
            self.raw_id_fields = list(self.raw_id_fields)
            self.raw_id_fields.append(db_field.name)

        return fields.AdminTagsInputField(**kwargs)


class TagsInputAdmin(TagsInputMixin, admin.ModelAdmin):
    pass


class TagsInputTabularInline(TagsInputMixin, admin.TabularInline):
    pass


class TagsInputStackedInline(TagsInputMixin, admin.StackedInline):
    pass


