from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.api_models.response import MovieResponse, Movie
from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def _aggregate_person(self, role):
        return ArrayAgg(
            'persons__full_name',
            filter=Q(personfilmwork__role=role),
            distinct=True
        )

    def get_queryset(self):
        return Filmwork.objects.annotate(
            actors=self._aggregate_person(
                PersonFilmwork.RoleTypes.actor),
            directors=self._aggregate_person(
                PersonFilmwork.RoleTypes.director),
            writers=self._aggregate_person(
                PersonFilmwork.RoleTypes.writer)
        ).values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'actors',
            'directors',
            'writers',
            genre=ArrayAgg(
                'genres__name',
                filter=Q(genres__name__isnull=False),
                distinct=True
            )
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset=list(queryset),
            page_size=50
        )

        return MovieResponse(
            count=paginator.count,
            total_pages=paginator.num_pages,
            prev=page.previous_page_number() if page.has_previous() else None,
            next=page.next_page_number() if page.has_next() else None,
            results=queryset
        ).dict()


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return Movie(**kwargs.get('object')).dict()
