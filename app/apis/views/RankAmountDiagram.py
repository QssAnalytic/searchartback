from core.models import Country

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict
from django.forms import model_to_dict

# diagram 3 and 4 display country name,code and code_2 and change of their ranks and amounts  
# data for chosen countries over all available years, by given indicator.
class RankAmountDiagrams(APIView):
    def get(self, request):
        
        indicator_name =  request.GET.get('indicator')
        countries = str(request.GET.get('countries')).split(';')
        year = int(request.GET.get('year1'))
        ranks = list(map(int,str(request.GET.get('ranks')).split(',')))

        queryset = Country.objects.select_related('indicator')\
        .filter(indicator__indicator=indicator_name,country__in=countries, rank__range=ranks)
        result = {}
        amount_list = []
        rank_list = []
        year_list = set()
        result['countries_data'] = []
        
      
        result = defaultdict(list)
        country_data_dict = defaultdict(list)

        for data in queryset:
            country_data_dict[data.country].append({
                'Country': data.country,
                'Country_code_2': data.country_code2,
                'Year': data.year,
                'Rank': data.rank,
                'Amount': float(data.amount)  # Convert amount to float
            })
            
            amount_list.append(float(data.amount))
            year_list.add(int(data.year))


        for country, data_list in country_data_dict.items():
            result['countries_data'].append({'country': data_list})

        # Calculate min, max, etc.
        result['min_rank'] = min(ranks,default="EMPTY")
        result['max_rank'] = max(ranks,default="EMPTY")
        result['min_amount'] = min(amount_list,default="EMPTY")
        result['max_amount'] = max(amount_list,default="EMPTY")
        result['year1'] = min(year_list,default="EMPTY")
        result['year2'] = max(year_list,default="EMPTY")
        
        return Response(result, status=status.HTTP_200_OK)