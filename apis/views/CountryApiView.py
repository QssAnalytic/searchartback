from rest_framework.views import APIView
from core.models import Country
from apis.serializers import CountrySerializer
from rest_framework.response import Response
from operator import itemgetter

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

class CountryApiView(APIView):
    serializer_class = CountrySerializer
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'indicator',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Gross Domestic Product billions of U.S. dollars"
                
            )
        ],responses={200: ""},
    )

    def get(self, request):
        indicator = request.GET.get("indicator")

        queryset = (
            Country.objects.select_related('indicator').filter(indicator__indicator=indicator)
            .order_by("country")
            .values_list("country", flat=True)
            .distinct()
        )

        response_data = [{"subsector": subsector} for subsector in queryset]

        combined_response = {}
        for data in response_data:
            subsector_name = data["subsector"]
            combined_response[subsector_name] = subsector_name

        return Response(combined_response.values())
