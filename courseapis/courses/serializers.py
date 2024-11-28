from rest_framework import serializers
from unicodedata import category

from courses.models import Category, Course, Lesson, Tag

class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, course):
        request = self.context.get('request')
        if request and course.image:
            return request.build_absolute_uri('/static/%s' % course.image)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CourseSerializer(BaseSerializer):


    class Meta:
        model = Course
        fields = ['id', 'subject', 'image','created_date', 'updated_date', 'category_id']


class LessonSerializer(BaseSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'course_id']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many = True)
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']