from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Avg, Max
from apis.utils.country_score import country_score
from operator import itemgetter


class SectorAverageScoreApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        year = request.GET.get("year")
        
        max_indecator_rank = (
            Country.objects.filter(year=year)
            .select_related("indicator")
            .values("rank","country").values("indicator__indicator").annotate(max_rank = Max('rank'))
        )
        country_rank = (
            Country.objects.filter(year=year, country=country)
            .select_related("indicator")
            .values("rank", "indicator__indicator")
        )
        average_score = country_score(max_indecator_rank=max_indecator_rank,
                                      country_rank=country_rank)

        return Response({"country": country, "average_score": average_score})

