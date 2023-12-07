from collections import defaultdict
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max, Subquery, OuterRef


class SectorYearScoreApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        sector = request.GET.get("sector")
        country = request.GET.get("country")
        
        queryset = Country.objects\
            .select_related('indicator')\
            .filter(country=country,indicator__subsector__sector__sector=sector)\
            .values("rank","year")
        
        year_rank_dict = defaultdict(list)
        
        for data in queryset:
            rank = data['rank']
            year = data['year']
            
            year_rank_dict[year].append(rank)

        max_rank_dict = {}
        for year,ranks in year_rank_dict.items():
            max_rank_dict[year] = max(ranks)
        
        year_scores = []
        for year, ranks in year_rank_dict.items():
            total_score = 0
            count = 0
            for rank in ranks:
                max_rank = max_rank_dict[year]
                score = round((1 - rank / max_rank) * 100, 2)
                total_score += score
                if score!=0:
                    count += 1
            
            if count==0:
                continue
            average_score = round(total_score / count, 2)
            
            # if year=="2019":
            #     print('year',year,'total',total_score,"count", count)
            year_scores.append({'year': year, "score":average_score})

        #evvelki kod
        '''
        max_rank_subquery = (
            Country.objects.filter(
                indicator__indicator=OuterRef("indicator__indicator"),
                indicator__subsector__sector__sector=sector,
                country=country,
            )
            .values("indicator__indicator")
            .annotate(max_rank=Max("rank"))
            .values("max_rank")
        )

        queryset = (
            Country.objects.filter(
                indicator__subsector__sector__sector=sector, country=country
            )
            .annotate(max_rank=Subquery(max_rank_subquery))
            .values("rank", "indicator__subsector__sector__sector", "max_rank", "year")
            .prefetch_related("indicator")
        )

        sector_data = {}
        for data in queryset:
            rank = data["rank"]
            max_rank = data["max_rank"]
            year = data["year"]

            if rank == 0:
                continue

            score = round((1 - rank / max_rank) * 100, 2)

            if score == 0:
                continue

            if year not in sector_data:
                sector_data[year] = score
            elif score > sector_data[year]:
                sector_data[year] = score
'''
        # result = [{"year": year, "score": score} for year, score in year_scores]

        year_scores.sort(key=lambda x: x["year"])

        return Response(year_scores)
