from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

from core.models import Sect, SubSect


class SectSubsectIndicaView(APIView):
    def get(self, request):
        try:
            sectors_data = (
                Sect.objects.prefetch_related(
                    Prefetch('subsectors', queryset=SubSect.objects.prefetch_related('indicator'))
                )
                .values('sector', 'subsect__subsector', 'subsect__indica__indicator')
            )
            sectors = {}
            
            for sector in sectors_data:
                sector_name = sector['sector']
                subsector_name = sector['subsect__subsector']
                indicator_name = sector['subsect__indica__indicator']

                if sector_name not in sectors:
                    sectors[sector_name] = {}
                
                if subsector_name not in sectors[sector_name]:
                    sectors[sector_name][subsector_name] = []
                
                sectors[sector_name][subsector_name].append(indicator_name)
            try:
                data = {
                    "sectors": sectors,
                    "default_choices":[Sect.objects.get(sector='Economy').id,0,0]
                }
                return Response(data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response("there are no Sectors matching query.", status=status.HTTP_404_NOT_FOUND)
        
        except ObjectDoesNotExist:
            return Response("there are no Sectors matching query.", status=status.HTTP_404_NOT_FOUND)

