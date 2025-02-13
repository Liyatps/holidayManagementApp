from django.shortcuts import render
import os
import requests
from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from dotenv import load_dotenv
from .serializers import HolidaySerializer

# Create your views here.

load_dotenv()
CALENDARIFIC_API_KEY = os.getenv("")

@api_view(['GET'])
def get_holidays(request):
    country_code=request.GET.get('country')
    year=request.GET.get('year')

    if not country_code or not year:
        return Response({"error": "country and year are required"}, status=status.HTTP_400_BAD_REQUEST)

    cache_key=f"holidays_{country_code}_{year}"
    cached_data=cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    url=f"https://calendarific.com/api/v2/holidays?api_key={CALENDARIFIC_API_KEY}&country={country_code}&year={year}"
    try:
        response=requests.get(url)
        response.raise_for_status()
        data=response.json()
        holidays=data.get('result',[])

        serializer=HolidaySerializer(holidays, many=True)

        cache.set(cache_key, serializer.data, timeout=86400)
        return Response(serializer.data)
    
    except requests.exceptions.RequestException as e:
        return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_holidays(request):
    query=request.GET.get('q')
    country_code=request.GET.get('country')
    year=request.GET.get('year')

    if not query or not country_code or not year:
        return Response({"error": "Query, country and year are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    cache_key=f"holidays_{country_code}_{year}"
    cached_data=cache.get(cache_key)

    if cached_data:
        filtered_holidays=[holiday for holiday in cached_data if query.lower() in holiday['name'].lower()]
        return Response(filtered_holidays)
    else:
        return Response({"error": "Holidays not found. "}, status=status.HTTP_404_NOT_FOUND)

        



