from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork, Roles


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        return (
            self.model.objects.all()
            .values(
                "id",
                "title",
                "description",
                "creation_date",
                "rating",
                "type",
            )
            .annotate(
                genres=ArrayAgg("genres__name", distinct=True),
                actors=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role=Roles.ACTOR),
                ),
                directors=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role=Roles.DIRECTOR),
                ),
                writers=ArrayAgg(
                    "persons__full_name",
                    distinct=True,
                    filter=Q(personfilmwork__role=Roles.WRITER),
                ),
            )
            .order_by("id")
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        return dict(queryset.filter(id=self.kwargs["pk"]).first())


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        prev_page = None
        next_page = 2

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        if cur_page := self.request.GET.get("page"):
            cur_page = int(cur_page) if cur_page != "last" else paginator.num_pages
            prev_page = cur_page - 1 if cur_page - 1 >= 1 else None
            next_page = cur_page + 1 if cur_page + 1 <= paginator.num_pages else None

        return {
            "count": paginator.count,
            "per_page": paginator.per_page,
            "total_pages": paginator.num_pages,
            "prev": prev_page,
            "next": next_page,
            "results": list(page),
        }
