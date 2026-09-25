from rest_framework.pagination import PageNumberPagination

from api.constants import PAGE_SIZE_ON_DEFAULT


class Pagination(PageNumberPagination):
    """Пагинация для списка пользователей."""

    page_size = PAGE_SIZE_ON_DEFAULT
    page_size_query_param = 'limit'
