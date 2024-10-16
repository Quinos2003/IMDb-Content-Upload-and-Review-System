import csv
from io import TextIOWrapper
from django.db.models import Q, Value
from django.db.models.functions import Cast
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from .models import Movie
from .serializers import MovieSerializer

# Custom filter to filter by year of release
class MovieFilter(FilterSet):
    release_year = filters.NumberFilter(field_name='release_date', lookup_expr='year')
    languages = filters.CharFilter(method='filter_languages')

    class Meta:
        model = Movie
        fields = ['release_date', 'release_year']

    def filter_languages(self, queryset, name, value):
        """
        Custom filter to handle languages dynamic filtering.
        Here, we will use Q objects to handle JSON fields.
        """
        # Using Q objects to filter the languages
        # return queryset.filter(Q(languages__contains=[value]) | Q(languages__contains=value))
        return queryset.filter(languages__contains=value)

# View for uploading movies data through a CSV file
class UploadCSVView(APIView):
    parser_classes = [MultiPartParser]  # Allows parsing of multi-part form data, such as file uploads

    def post(self, request, *args, **kwargs):
        # Ensure that a file is provided in the request
        if 'file' not in request.FILES:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Read and decode the uploaded CSV file
        file = request.FILES['file']
        decoded_file = TextIOWrapper(file, encoding='utf-8')
        csv_reader = csv.DictReader(decoded_file)

        movies_to_create = []  # Store valid Movie instances for bulk creation
        errored_rows = []  # Store rows that failed validation with error messages
        
        # Process each row in the CSV file
        for counter, row in enumerate(csv_reader, start=1):  # Start counter at 1 for readability
            print(f"Processing row {counter}")

            # Validate the current row
            validation_error = self.validate_row(row)
            if validation_error:
                # Log any validation errors
                errored_rows.append({
                    "row": counter,
                    "error": validation_error,
                    "data": row
                })
                print(f"Error in row {counter}: {validation_error}")
                continue  # Skip the row if there are validation errors

            # Create a Movie instance using the valid data from the row

            # print(row.get('languages'))
            languages = eval(row.get('languages'))
            movie = Movie(
                budget=row.get('budget'),
                homepage=row.get('homepage'),
                original_language=row.get('original_language'),
                original_title=row.get('original_title'),
                overview=row.get('overview'),
                release_date=row.get('release_date') or None,  # Handle cases where release_date is empty
                revenue=row.get('revenue'),
                runtime=row.get('runtime'),
                status=row.get('status'),
                title=row.get('title'),
                vote_average=row.get('vote_average'),
                vote_count=row.get('vote_count'),
                production_company_id=row.get('production_company_id'),
                genre_id=row.get('genre_id'),
                languages=','.join(languages) # Convert list of languages to a comma-separated string
                
            )
            movies_to_create.append(movie)

        # Bulk create all valid movie records
        if movies_to_create:
            Movie.objects.bulk_create(movies_to_create)

        # Prepare response data
        response_data = {
            "message": "Movies data upload completed",
            "successful_rows": len(movies_to_create),
            "failed_rows": len(errored_rows),
            "errors": errored_rows,  # Include details about rows that failed validation
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def validate_row(self, row):
        errors = []
        required_fields = ['title', 'original_title', 'budget', 'revenue', 'runtime']

        for field in required_fields:
            if not row.get(field):
                errors.append(f"{field} is required.")

        if row.get('release_date') and not self.is_valid_date(row['release_date']):
            errors.append("release_date must be in YYYY-MM-DD format.")
        
        # Ensure languages are a valid JSON list
        try:
            languages = eval(row.get('languages', '[]'))
            if not isinstance(languages, list):
                raise ValueError
        except (SyntaxError, ValueError):
            errors.append("languages must be a valid list of strings.")
        
        return errors if errors else None

    def is_valid_date(self, date_str):
        """Check if the date string is in YYYY-MM-DD format."""
        from datetime import datetime
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False


# Pagination class for movie listings, allowing control over the number of records returned per page
class MoviePagination(PageNumberPagination):
    page_size = 10  # Default number of movies per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size via query parameter
    max_page_size = 100  # Limit the maximum page size


# View for listing movies with filtering and sorting capabilities
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()  # queryset to fetch all movie records
    serializer_class = MovieSerializer  # Use the MovieSerializer to serialize movie objects
    pagination_class = MoviePagination  # Paginate results using the custom pagination class
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Enable filtering and ordering functionality
    filterset_class = MovieFilter  # Use custom filterset to allow filtering by year
    ordering_fields = ['release_date', 'vote_average']  # Fields available for ordering (ascending or descending)
