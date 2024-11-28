from django.contrib.admin.templatetags.admin_list import pagination
from rest_framework import viewsets,generics
from unicodedata import category
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson
from courses import serializers, paginators
from courses.serializers import LessonDetailsSerializer


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active = True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePagination

    def get_queryset(self):
        query = self.queryset

        q = self.request.query_params.get("q")

        cate_id = self.request.query_params.get("category_id")

        if cate_id:
            query = query.filter(category_id = cate_id)
        if q:
            query = query.filter(subject__icontains =q)

        return query

    @action(methods=['get'],detail= True,url_path='lessons')
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        return Response (serializers.LessonSerializer(lessons, many= True, context={'request': request}).data)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active = True)
    serializer_class = LessonDetailsSerializer