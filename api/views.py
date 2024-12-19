from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .Strategies.Load_Data import get_options
from .Strategies.BlackScholes import evaluate_call_option

@api_view(['GET', 'POST'])
def options_view(request, ticker):
    if request.method == 'GET':
        options_data = get_options(ticker)
        if options_data is None:
            return Response({"error": f"Error getting options for {ticker}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(options_data)
    elif request.method == 'POST':
        option_data = request.data
        if not option_data:
            return Response({"error": "No option data provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            evaluation_result = evaluate_call_option(option_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(evaluation_result)

@api_view(['POST'])
def option_detail_view(request):
    option_data = request.data
    if not option_data:
        return Response({"error": "No option data provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        evaluation_result = evaluate_call_option(option_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(evaluation_result)
