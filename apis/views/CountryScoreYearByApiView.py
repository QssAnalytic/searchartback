from collections import defaultdict
import json
from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Avg, Max
from django.core.serializers.json import DjangoJSONEncoder
from operator import itemgetter





class CountryScoreYearByApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")    
        max_indecator_rank = (
            Country.objects.all()
            .select_related("indicator")
            .values("rank","country", "year").values("indicator__indicator","year").annotate(max_rank = Max('rank'))
        )

        country_rank = (
            Country.objects.filter(country=country)
            .select_related("indicator")
            .values("indicator__indicator","year", 'country').annotate(max_rank = Max('rank'))
        ) 

        result = {}
        response_data = []
        obj = {}
        
        for entry in max_indecator_rank:
            year = entry["year"]
            indicator = entry["indicator__indicator"]
            max_rank = entry["max_rank"]
            
            if year not in result:
                result[year] = {}

            result[year][indicator] = max_rank

        for con_data in country_rank:
            con_max_rank = con_data['max_rank']
            max_indcator_rank = result[con_data['year']][con_data['indicator__indicator']]
            score = round((1 - con_max_rank / max_indcator_rank) * 100, 2)
            if con_data['year'] not in obj:
                obj[con_data['year']] = {}
                obj[con_data['year']]['score'] = score
                obj[con_data['year']]['count'] = 1

            else:
                obj[con_data['year']]['score']+=score
                obj[con_data['year']]['count']+=1

        for year, avg in obj.items():
            response_data.append(
                {
                    "year": year,
                    "average_score": round(avg['score'] / avg['count'], 2),
                }
            )
        response_data = sorted(response_data, key=itemgetter("year"))
            
        return Response(response_data)