from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

from .models import Dataset
from .analytics import analyze_equipment_json
import logging

class UploadCSVView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data

            if not isinstance(data, list):
                return Response(
                    {"error": "Expected a JSON array of equipment records"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(data) == 0:
                return Response(
                    {"error": "Dataset cannot be empty"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            required_keys = {
                "Equipment Name",
                "Type",
                "Flowrate",
                "Pressure",
                "Temperature",
            }

            for idx, row in enumerate(data):
                if not isinstance(row, dict):
                    return Response(
                        {"error": f"Row {idx} is not a valid object"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                missing = required_keys - row.keys()
                if missing:
                    return Response(
                        {"error": f"Row {idx} missing fields", "missing": list(missing)},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            try:
                summary = analyze_equipment_json(data)
            except Exception as e:
                logging.exception("Error analyzing equipment JSON")
                return Response(
                    {"error": "Failed to analyze dataset", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            try:
                dataset = Dataset.objects.create(
                    name=f"dataset_{Dataset.objects.count() + 1}",
                    raw_data=data,
                    summary=summary,
                )
            except Exception as e:
                logging.exception("Error saving dataset to database")
                return Response(
                    {"error": "Failed to save dataset", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            try:
                old_datasets = Dataset.objects.order_by("-uploaded_at")[5:]
                if old_datasets.exists():
                    Dataset.objects.filter(pk__in=[d.pk for d in old_datasets]).delete()
            except Exception:
                logging.exception("Error deleting old datasets")

            return Response(
                {"id": dataset.id, **summary},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logging.exception("Unexpected error in UploadCSVView")
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DatasetHistoryView(APIView):
    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 5))
            if limit > 10:
                limit = 10
        except ValueError:
            return Response({"error": "Invalid limit parameter. Must be an integer."}, status=400)
        
        try:
            datasets = Dataset.objects.order_by('-uploaded_at')[:limit]
            data = []
            for d in datasets:
                try:
                    preview = d.summary.get('preview', [])[:3] if d.summary else []
                    file_size = d.file.size if d.file else None
                    data.append({
                        "id": d.id,
                        "name": d.name,
                        "uploaded_at": d.uploaded_at,
                        "summary": d.summary,
                        "file_size": file_size,
                        "preview": preview
                    })
                except Exception as e:
                    # Log the error if needed, but skip this dataset
                    continue
        except Exception as e:
            return Response({"error": f"An error occurred while retrieving datasets. {str(e)}" }, status=500)
        
        return Response(data)
