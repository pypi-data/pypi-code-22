from haystack import indexes


from datetime import datetime
from django.utils.html import strip_tags, strip_entities

from tendenci.apps.stories.models import Story
from tendenci.apps.perms.object_perms import ObjectPermission
from tendenci.apps.categories.models import Category
from tendenci.apps.perms.indexes import TendenciBaseSearchIndex


class StoryIndex(TendenciBaseSearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    start_dt = indexes.DateTimeField(model_attr='start_dt', null=True)
    end_dt = indexes.DateTimeField(model_attr='end_dt', null=True)
    expires = indexes.BooleanField(model_attr='expires', null=True)

    # categories
    category = indexes.CharField()
    sub_category = indexes.CharField()

    # RSS fields
    can_syndicate = indexes.BooleanField(null=True)

    @classmethod
    def get_model(self):
        return Story

    def prepare_content(self, obj):
        content = obj.content
        content = strip_tags(content)
        content = strip_entities(content)
        return content

    def prepare_category(self, obj):
        category = Category.objects.get_for_object(obj, 'category')
        if category:
            return category.name
        return ''

    def prepare_sub_category(self, obj):
        category = Category.objects.get_for_object(obj, 'sub_category')
        if category:
            return category.name
        return ''

    def prepare_can_syndicate(self, obj):
        return obj.syndicate and obj.status == 1 and obj.status_detail == 'active' \
                and datetime.now() > obj.end_dt
