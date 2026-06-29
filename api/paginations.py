from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):  # custom pagination - controls how list results are split into pages
    page_size_query_param = 'page_size'  # lets client choose page size via ?page_size=10
    page_query_param = 'page_number'  # client requests a page via ?page_number=2 (instead of default ?page=2)
    max_page_size = 2  # hard limit - client can never request more than 2 items per page

    def get_paginated_response(self, data):  # customizes the shape of the paginated response
        return Response({
            'next': self.get_next_link(),  # URL to the next page (None if no next page)
            'previous': self.get_previous_link(),  # URL to the previous page (None if no previous page)
            'count': self.page.paginator.count,  # total number of records across all pages
            'page_size': self.page_size,  # how many items are in this page
            'results': data  # the actual list of items for this page
        })