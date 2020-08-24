from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import FieldError
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.db.models import Q
from functools import reduce
from operator import or_

from rest_framework.settings import api_settings


class GeneralMixin(ListModelMixin):
    ordering_param = api_settings.ORDERING_PARAM
    page_param = "page"

    class Meta:
        abstract = True

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self._order(queryset, request.GET)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _order(self, queryset, query_params):
        params = query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(",")]
            queryset = queryset.order_by(*fields)
        return queryset

    def _paginate(self, queryset, request):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                instance=page, context={"request": request}, many=True
            )
            return self.get_paginated_response(serializer.data)

        return self.get_serializer(
            instance=queryset, context={"request": request}, many=True
        )

    def get_processed_queryset(self, query_params):
        pass


class FilterWithBooleanMixin(GeneralMixin):
    OR = "|"

    def list(self, request, *args, **kwargs):
        if not self._is_request_with_booleans(request):
            return super().list(request, kwargs)

        queryset = self.get_processed_queryset(request.GET)
        queryset = self._order(queryset, request.GET)
        serializer = self._paginate(queryset, request)
        return Response(serializer.data)

    def get_processed_queryset(self, query_params):
        queries = self._parse_expressions(query_params)
        queryset = self.get_queryset()
        # perform AND
        for q in queries:
            if not q:
                continue
            # perform OR
            query = reduce(or_, q)
            queryset = queryset.filter(query)
        return queryset.distinct()

    def _parse_expressions(self, query_params):
        queries = []
        fields = [
            key
            for key in query_params.keys()
            if key not in [self.ordering_param, self.page_param]
        ]
        for field in fields:
            expressions = query_params.getlist(field)
            if not expressions or all(v == "" for v in expressions):
                continue
            for exp in expressions:
                values = exp.split(self.OR)
                queries.append([Q(**{field: val}) for val in values])
        return queries

    def _is_request_with_booleans(self, request):
        for key in request.GET.keys():
            values = request.GET.getlist(key)
            if not values or all(v == "" for v in values):
                continue
            if len(values) > 1 or any(self.OR in v for v in values):
                return True
        return False


class SearchNameMixin(GeneralMixin):
    SEARCH_FIELD = "school_name"

    def list(self, request, *args, **kwargs):
        queryset = self.get_processed_queryset(request.GET)
        queryset = self._order(queryset, request.GET)
        serializer = self._paginate(queryset, request)
        return Response(serializer.data)

    def get_processed_queryset(self, query_params):
        queryset = self.filter_queryset(self.get_queryset())

        if self.SEARCH_FIELD in query_params:
            name = query_params.get(self.SEARCH_FIELD)
            queryset = self._search(queryset, name)
        return queryset

    def _search(self, queryset, name):
        return (
            queryset.annotate(similarity=TrigramSimilarity(self.SEARCH_FIELD, name))
            .filter(similarity__gte=0.05)
            .order_by("-similarity")
        )

    def _is_request_with_search(self, request):
        return request.GET.get(self.SEARCH_FIELD) is not None


class FilterWithBooleanAndSearchMixin(FilterWithBooleanMixin, SearchNameMixin):
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_processed_queryset(request.GET)
        except (ValueError, FieldError) as e:
            return Response(f"Invalid query: {e}", 400)
        serializer = self._paginate(queryset, request)
        return Response(serializer.data)

    def get_processed_queryset(self, query_params):
        query_params = query_params.copy()
        search_expressions = query_params.pop(self.SEARCH_FIELD, None)
        queryset = super().get_processed_queryset(query_params)
        if search_expressions and any(v != "" for v in search_expressions):
            for exp in search_expressions:
                values = exp.split(self.OR)
                queryset = self._search(queryset, values[0])
        return self._order(queryset, query_params)
