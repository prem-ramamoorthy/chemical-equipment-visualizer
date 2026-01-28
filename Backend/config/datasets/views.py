from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Dataset
from .utils import analyze_csv


class UploadCSVView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES["file"]

        dataset = Dataset.objects.create(
            name=file.name,
            file=file,
            summary={}
        )

        summary, preview = analyze_csv(dataset.file.path)
        dataset.summary = summary
        dataset.save()

        # Keep only last 5
        Dataset.objects.order_by('-uploaded_at')[5:].delete()

        return Response({
            "summary": summary,
            "preview": preview
        })

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
