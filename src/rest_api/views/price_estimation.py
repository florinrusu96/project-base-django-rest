from rest_framework import views
from rest_framework.response import Response

from rest_api.prediction import prediction_utils


class PriceEstimationView(views.APIView):

    def get(self, request):
        # For now, the algorithm does not take the date into account
        date = request.query_params.get('date', None)
        stock_name = request.query_params.get('stock_name', None)
        if not date:
            return Response(data={'message': 'Date not provided'}, status=400)
        if not stock_name:
            return Response(data={'message': 'Stock name not provided'}, status=400)
        stock_prediction = prediction_utils.get_prediction(stock_name=stock_name)
        return Response(data={'stock_prediction': stock_prediction, 'stock_name': stock_name}, status=200)
