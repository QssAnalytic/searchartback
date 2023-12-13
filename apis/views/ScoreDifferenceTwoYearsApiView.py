from collections import defaultdict
from pprint import pprint
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter
from django.db.models import Avg, Max
from apis.utils.country_score import country_score



class ScoreDifferenceTwoYearsApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        year1 = request.GET.get("year1")  # First year
        year2 = request.GET.get("year2")  # Second year
        
        max_indecator_rank1 = (
            Country.objects.filter(year=year1)
            .select_related("indicator")
            .values("rank","country").values("indicator__indicator").annotate(max_rank = Max('rank'))
        )
        
        country_rank1 = (
            Country.objects.filter(year=year1, country=country)
            .select_related("indicator")
            .values("rank", "indicator__indicator", "country_code")
        )
        country_code = country_rank1[0]['country_code']
        max_indecator_rank2 = (
            Country.objects.filter(year=year2)
            .select_related("indicator")
            .values("rank","country").values("indicator__indicator").annotate(max_rank = Max('rank'))
        )
        country_rank2 = (
            Country.objects.filter(year=year2, country=country)
            .select_related("indicator")
            .values("rank", "indicator__indicator")
        )
        avarage_score1 = country_score(max_indecator_rank=max_indecator_rank1, country_rank=country_rank1)
        avarage_score2 = country_score(max_indecator_rank=max_indecator_rank2, country_rank=country_rank2)
        score_difference = round((avarage_score2 - avarage_score1),2)

        response_data = {
            "country": country,
            "score_difference": score_difference,
            "country_code": country_code,
        }
        return Response(response_data)


# class ScoreTestDifferenceTwoYearsApiView(APIView):
#     serializer_class = CountrySerializer

#     def get(self, request):
#         country = request.GET.get("country")
#         year1 = request.GET.get("year1")  # First year
#         year2 = request.GET.get("year2")  # Second year
        
#         max_indecator_rank1 = (
#             Country.objects.filter(year=year1)
#             .select_related("indicator")
#             .values("rank","country").values("indicator__indicator").annotate(max_rank = Max('rank'))
#         )
#         country_rank1 = (
#             Country.objects.filter(year=year1, country=country)
#             .select_related("indicator")
#             .values("rank", "indicator__indicator", "country_code")
#         )
#         country_code = country_rank1[0]['country_code']
#         max_indecator_rank2 = (
#             Country.objects.filter(year=year2)
#             .select_related("indicator")
#             .values("rank","country").values("indicator__indicator").annotate(max_rank = Max('rank'))
#         )
#         country_rank2 = (
#             Country.objects.filter(year=year2, country=country)
#             .select_related("indicator")
#             .values("rank", "indicator__indicator")
#         )
#         avarage_score1 = country_score(max_indecator_rank=max_indecator_rank1, country_rank=country_rank1)
#         avarage_score2 = country_score(max_indecator_rank=max_indecator_rank2, country_rank=country_rank2)
#         score_difference = avarage_score2 - avarage_score1

#         response_data = {
#             "country": country,
#             "score_difference": score_difference,
#             "country_code": country_code,
#         }
#         return Response(response_data)