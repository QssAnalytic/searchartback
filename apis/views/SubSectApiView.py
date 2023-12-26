from rest_framework.views import APIView
from core.models import SubSect
from apis.serializers import SubSectSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

class SubSectApiView(APIView):
    serializer_class = SubSectSerializer
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'sector',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Economy",
                default="Economy"
                
            )
        ],responses={200: ""},
    )
    def get(self, request, pk=None):
        sector = request.GET.get("sector")
        subsector = SubSect.objects.filter(sector__sector=sector)

        response_data = []

        for subsect in subsector:
            response_data.append(subsect.subsector)

        return Response(response_data)
