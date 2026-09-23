from rest_framework.pagination import PageNumberPagination

from .constants import PAGE_SIZE_ON_DEFAULT, PAGE_SIZE_ON_MAIN


class UserPagination(PageNumberPagination):
    page_size = PAGE_SIZE_ON_DEFAULT
    page_size_query_param = 'limit'


class RecipePagination(PageNumberPagination):
    page_size = PAGE_SIZE_ON_MAIN
    page_size_query_param = 'limit'
