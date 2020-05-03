from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.db.models import Q
from functools import reduce
from operator import or_


class FilterWithBooleanMixin(ListModelMixin):
    OR = "|"

    def list(self, request, *args, **kwargs):
        if not self._is_request_with_booleans(request):
            return super().list(request, kwargs)

        queryset = self._query_with_boolean(request.GET)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _query_with_boolean(self, query_params):
        queries = self._parse_expressions(query_params)
        queryset = self.get_queryset()
        # perform AND
        for q in queries:
            if not q:
                continue
            # perform OR
            query = reduce(or_, q)
            queryset = queryset.filter(query)
        return queryset

    def _parse_expressions(self, query_params):
        queries = []
        for field in query_params.keys():
            expressions = query_params.getlist(field)
            if not expressions or all(v == '' for v in expressions):
                continue
            for exp in expressions:
                values = exp.split(self.OR)
                queries.append([Q(**{field: val}) for val in values])
        return queries

    def _is_request_with_booleans(self, request):
        for key in request.GET.keys():
            values = request.GET.getlist(key)
            if not values or all(v == '' for v in values):
                continue
            if len(values) > 1 or any(self.OR in v for v in values):
                return True
        return False


class SearchNameMixin(ListModelMixin):
    SEARCH_FIELD = 'school_name'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self._is_request_with_search(request):
            name = request.GET.get(self.SEARCH_FIELD)
            queryset = self._search(queryset, name)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _search(self, queryset, name):
        return queryset \
                .annotate(similarity=TrigramSimilarity(self.SEARCH_FIELD, name)) \
                .filter(similarity__gte=0.05) \
                .order_by('-similarity')

    def _is_request_with_search(self, request):
        return request.GET.get(self.SEARCH_FIELD) is not None


class FilterWithBooleanAndSearchMixin(FilterWithBooleanMixin, SearchNameMixin):

    def list(self, request, *args, **kwargs):
        if not self._is_request_with_booleans(request) or not self._is_request_with_search(request):
            return super().list(request, args, kwargs)
        query_params = request.GET.copy()
        search_expressions = query_params.pop(self.SEARCH_FIELD, None)
        queryset = self._query_with_boolean(query_params)
        if search_expressions and any(v != '' for v in search_expressions):
            for exp in search_expressions:
                values = exp.split(self.OR)
                queryset = self._search(queryset, values[0])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


