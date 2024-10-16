# IMDb-Content-Upload-and-Review-System

This Django-based API allows IMDb's content team to upload movie/show data via CSV files, manage it in a database, and view it with pagination, filtering, and sorting options. It supports large CSV uploads and provides scalable movie data management.

## Features

- Upload movie/show data via CSV file
- View uploaded data with pagination, filtering by year and language, and sorting by release date or ratings
- Scalable and fast bulk data upload
- Admin interface for managing movie data
- RESTful APIs with Django Rest Framework

## Installation Steps

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/IMDb-Content-Upload-and-Review-System.git
cd IMDb-Content-Upload-and-Review-System
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate your dependencies:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

On Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

By default, this project uses SQLite. If you want to use PostgreSQL or another database, update the DATABASES setting in settings.py.

Run migrations to set up the initial database schema:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Create a Superuser (Admin Access)

To manage the content through the Django admin panel, create a superuser:

```bash
python3 manage.py createsuperuser
```

Follow the prompts to create the superuser.

### 6. Run the Development Server

Start the Django development server:

```bash
python3 manage.py runserver
```

The project will be available at http://127.0.0.1:8000/.

## API Endpoints

### 1. Upload CSV

- Endpoint: `/api/upload/`
- Method: POST
- Description: Upload movie data via CSV file.

Example curl request:

```bash
curl --location 'http://localhost:8000/api/movies/upload/' \
--form 'file=@"movies_data_assignment.csv;filename=movies_data_assignment.csv"'
```

### 2. List Movies

- Endpoint: `/api/movies/`
- Method: GET
- Description: Retrieve a paginated list of movies with optional filtering and sorting.

Filtering Options:
- `languages`: Filter by language (e.g., English, Français)
- `release_year`: Filter by year of release

Sorting Options:
- `release_date`: Sort by release date
- `vote_average`: Sort by rating

Example curl request:

```bash
# Get all movies, filter by language 'English', and sort by release_date
curl -X GET "http://127.0.0.1:8000/api/movies/?languages=English&ordering=-release_date"
```

### 3. Admin Panel

To access the admin panel:

- URL: http://127.0.0.1:8000/admin/
- Method: GET
- Login: Use the superuser credentials created in Step 5.

## Project Structure

```
.
├── content                     # Django app for movie content management
│   ├── migrations               # Database migrations
│   ├── models.py                # Models for Movies
│   ├── serializers.py           # Serializers for API views
│   ├── views.py                 # API views for uploading and listing movies
│   ├── urls.py                  # URL configurations for the content app
│   └── ...
├── imdb_content_system          # Main Django project folder
│   ├── settings.py              # Project settings
│   ├── urls.py                  # URL configuration for the project
│   └── ...
├── db.sqlite3                   # SQLite database file (default)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── ...
```

## Testing the APIs

You can test the APIs using Postman or curl.

1. Upload CSV: Send a POST request to http://127.0.0.1:8000/api/upload/ with form-data containing the CSV file.
2. List Movies: Send a GET request to http://127.0.0.1:8000/api/movies/ with optional query parameters like languages, release_year, and ordering.

## Postman Collection

A Postman collection is provided for easier testing of the APIs:

- File: `Samarth_Imdb_APIs.postman_collection.json`

To use:
1. Open Postman.
2. Import the collection file into Postman.
3. Run the pre-configured requests to interact with the API.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
