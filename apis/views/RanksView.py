from rest_framework.views import APIView
from django.db.models import Max, Min
from rest_framework.response import Response
from rest_framework import status

from core.models import Country

class AvailableRanksView(APIView):
    def get(self, request):
        indicator_name = request.GET.get('indicator')
        year = request.GET.get('year')

        queryset = Country.objects.select_related("indicator").filter(
            indicator__indicator=indicator_name,year=year
        ).aggregate(min_rank=Min('rank'), max_rank=Max('rank'))

        return Response(queryset, status=status.HTTP_200_OK)