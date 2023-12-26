from rest_framework.views import APIView
from django.db.models import Max, Min
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
from core.models import Country

class AvailableRanksView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'indicator',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Gross Domestic Product billions of U.S. dollars"
                
            ),
            openapi.Parameter(
                'year',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="2019"
                
            ),
            

        ],responses={200: ""},
        
    )
    def get(self, request):
        indicator_name = request.GET.get('indicator')
        year = request.GET.get('year')
        print(type(year))

        queryset = Country.objects.select_related("indicator").filter(
            indicator__indicator=indicator_name,year=year
        ).aggregate(min_rank=Min('rank'), max_rank=Max('rank'))

        return Response(queryset, status=status.HTTP_200_OK)