from django.conf.urls import include
from django.urls import path, re_path
from django.db.models import Q, Exists, OuterRef
from .views import generic, tracks, slack, users
from .models import Track, Artist, Rate
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'genres']


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = LimitOffsetPagination


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    artists = serializers.StringRelatedField(many=True)

    class Meta:
        model = Track
        fields = ['id', 'title', 'artists', 'album', 'popularity', 'populated']


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get'],
        detail=False,
        url_path='unrated',
        url_name='unrated_tracks'
    )
    def get_unrated(self, request):
        user = request.user
        try:
            limit = int(request.GET.get('limit', 10))
        except:
            limit = 10

        try:
            offset = int(request.GET.get('offset', 0))
        except:
            offset = 0

        max = offset + limit

        tracks = Track.objects.filter(
            ~Exists(
                Rate.objects.filter(
                    track=OuterRef('pk'),
                    user=user.id
                )
            )
        )[offset:max] if user.id else []

        serializer = TrackSerializer(tracks, many=True, context={'request': request})

        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=False,
        url_path='search',
        url_name='search_tracks'
    )
    def search(self, request):
        q = request.GET.get("q", default="")

        try:
            limit = int(request.GET.get('limit', 10))
        except:
            limit = 10

        try:
            offset = int(request.GET.get('offset', 0))
        except:
            offset = 0

        max = offset + limit

        tracks = Track.objects.filter(
            Q(title__icontains=q)
            | Q(album__icontains=q)
            | Q(artists__name__icontains=q)
        )[offset:max]

        serializer = TrackSerializer(tracks, many=True, context={'request': request})

        return Response(serializer.data)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'tracks', TrackViewSet)
router.register(r'artists', ArtistViewSet)

urlpatterns = [
    re_path(r'^$', generic.index, name='index'),
    re_path(r'^csv$', generic.dump, name='csv'),
    re_path(r'^tracks/playing$', tracks.playing, name='tracks_playing'),
    re_path(r'^tracks/?P(<id>\d+)/rate$', tracks.rate, name='tracks_rate'),
    re_path(r'^tracks/played$', tracks.played, name='tracks_played'),
    re_path(r'^tracks/populate$', tracks.populate, name='tracks_populate'),
    re_path(r'^tracks/queue$', tracks.queue, name='tracks_queue'),
    re_path(r'^tracks/dequeue$', tracks.dequeue, name='tracks_dequeue'),
    re_path(r'^tracks/top$', tracks.top, name='tracks_top'),
    re_path(r'^slack/subscribe$', slack.subscribe, name='slack_subscribe'),
    re_path(r'^slack/unsubscribe$', slack.unsubscribe, name='slack_unsubscribe'),
    re_path(r'^slack/interactive$', slack.interactive, name='slack_interactive'),
    re_path(r'^slack/notify$', slack.notify, name='slack_notify'),
    re_path(r'^slack/proxy$', slack.proxy, name='slack_proxy'),
    re_path(r'^users/populate$', users.populate, name='users_populate'),
    path('auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
