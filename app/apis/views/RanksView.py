from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Country

class AvailableRanksView(APIView):
    def get(self, request):
        indicator_name = request.GET.get('indicator')
        year = request.GET.get('year')

        queryset = Country.objects.select_related("indicator").filter(
            indicator__indicator=indicator_name,year=year
        )
        
        # get min and max rank
        ranks_list = []
        # print(queryset)
        for data in queryset:
            ranks_list.append(data.rank)
        
        result = {
            "min_rank": min(ranks_list, default="EMPTY"),
            "max_rank": max(ranks_list, default="EMPTY"),
        }

        return Response(result, status=status.HTTP_200_OK)