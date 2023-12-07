from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter


class CountryScoreYearByApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        
        queryset = (
            Country.objects.filter(country=country)
            .prefetch_related("indicator__subsector__sector")
            .values_list("year", "rank", "indicator__subsector__sector__sector")
        )

        year_rank_dict = defaultdict(list)
        for year, rank, sector in queryset:
            if sector not in year_rank_dict:
                year_rank_dict[sector] = {}

            if year not in year_rank_dict[sector]:
                year_rank_dict[sector][year] = []

            year_rank_dict[sector][year].append(rank)
        
        max_rank_dict = {}
        for sector, year_data in year_rank_dict.items():
            max_rank_year = {}  # Create a dictionary to store max ranks for each year in the sector
            for year, ranks in year_data.items():
                max_rank = max(ranks) if ranks else None  # Calculate the max rank, or None if no ranks are available
                max_rank_year[year] = max_rank
            max_rank_dict[sector] = max_rank_year  # Store the max rank data for the sector in max_rank_dict

        response_data = []
        year_scores = defaultdict(lambda: {"total_score": 0, "num_sectors": 0})

        for key_sector, value_year_rank_list in year_rank_dict.items():
            for year, ranks in value_year_rank_list.items():
                max_rank = max_rank_dict[key_sector].get(year, None)
                if max_rank is not None:
                    for rank in ranks:
                        if rank == 0:
                            continue
                        score = round((1 - rank / max_rank) * 100, 2)
                        if score != 0:
                            year_scores[year]["total_score"] += score
                            year_scores[year]["num_sectors"] += 1

        # Calculate the average score for each year
        for year, data in year_scores.items():
            if data["num_sectors"] == 0:
                average_score = 0
            else:
                average_score = round(data["total_score"] / data["num_sectors"], 2)

            response_data.append(
                {
                    "year": year,
                    "average_score": average_score,
                }
            )

        response_data = sorted(response_data, key=itemgetter("year"))

        return Response(response_data)
