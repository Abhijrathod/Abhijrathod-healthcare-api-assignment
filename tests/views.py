from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Min, Max, Avg, Count, Q
from .models import TestResult
from .serializers import TestResultSerializer


class TestResultCreateView(APIView):
    """
    POST endpoint to create a new test record.
    Expects JSON with fields:
    - patient_id (int)
    - test_name (str): One of ['GLUCOSE', 'HB', 'CHOL']
    - value (float/decimal)
    - unit (str)
    - test_date (ISO 8601 format string)
    - is_abnormal (bool)
    """

    def post(self, request):
        # Validate incoming data using the serializer
        serializer = TestResultSerializer(data=request.data)
        if serializer.is_valid():
            # Save the valid test result
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return validation errors with a 400 Bad Request status
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PatientTestResultsView(APIView):
    """
    GET endpoint to retrieve all test results for a specific patient.
    Query parameter: `patient_id` (int)
    """

    def get(self, request):
        # Extract `patient_id` from query parameters
        patient_id = request.query_params.get('patient_id')

        # If `patient_id` is not provided, return a 400 Bad Request error
        if not patient_id:
            return Response({"detail": "Patient ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that `patient_id` is a valid integer
        try:
            patient_id = int(patient_id)
        except ValueError:
            return Response({"detail": "Patient ID must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch test results for the given `patient_id`
        tests = TestResult.objects.filter(patient_id=patient_id)

        # If no tests are found, return an empty response
        if not tests.exists():
            return Response({"detail": "No test results found for the given patient ID."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the test data
        serializer = TestResultSerializer(tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestStatsView(APIView):
    """
    GET endpoint to retrieve basic statistics (min, max, avg) for each test type.
    Also provides the count of abnormal tests for each type.
    """

    def get(self, request):
        # Aggregate statistics for all test types
        stats = TestResult.objects.values('test_name').annotate(
            min_value=Min('value'),
            max_value=Max('value'),
            avg_value=Avg('value'),
            total_tests=Count('id'),
            abnormal_count=Count('id', filter=Q(is_abnormal=True))
        )

        # Return the aggregated statistics
        return Response({"test_stats": stats}, status=status.HTTP_200_OK)
