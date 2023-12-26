from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

class YearApiView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'countries',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Afghanistan;Albania;Algeria;Andorra;Angola;Antigua and Barbuda;Argentina"
                
            ),
            openapi.Parameter(
                'indicator',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Gross Domestic Product billions of U.S. dollars"
                
            ),
            

        ],responses={200: ""},
        
    )
    def get(self, request):
        countries = str(request.GET.get("countries")).split(";")
        indicator = request.GET.get("indicator")
        queryset = (
            Country.objects.select_related('indicator').filter(country__in=countries, indicator__indicator=indicator)
            .values("year")
            .distinct()
        )

        years = []
        for year_dict in queryset:
            years.append(year_dict['year'])
        years = sorted(years)

        return Response(years)