# URL Shortener

A URL shortening service with REST API to generate shortened urls, look up original url from short url and redirect shortened URLs.

All link accesses are recorded with a click count variable.
## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package installer)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jamesl28/URL-Shorten.git
   cd urlshortener
   ```
   
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   # On Windows: 
   venv/Scripts/activate
   ```
   
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```
5. **Start the development server**
   ```bash
   python manage.py runserver
   ```
6. **Create a superuser** (optional, not necessary for swagger)
   ```bash
   python manage.py createsuperuser
   ```

7. **Access the application**
   - Admin panel: http://127.0.0.1:8000/admin/
   - API documentation: http://127.0.0.1:8000/swagger/

## API Usage
1. **Shorten URL**: `POST /api/shorten/`
   - Accepts a JSON object with an `original_url` field
   - Returns the original URL, shortened URL, and initial click count (0)

2. **Look up URL**: `GET /api/lookup/<short_url>/`
   - Returns details about a shortened URL including original destination and click count

3. **Redirect**: `GET /<short_url>/`
   - Redirects to the original URL
   - Automatically increments the click counter
     
## Design Considerations and Enhancements

* **Database** - For simplicity and the scope of the project I used SQLite. In a production environment this would be replaced with a more complete database such as PostgreSQL, which would be faster and handle higher traffic.
* **URL Generation** - Using a base64 encoding with a length of 7 digits provides about 4 trillion unique shortened URLS. This should be quite sufficient and could potentially be reduced if a shorter url is desired.
* **Collisions** -  Collisions are automatically handled by increasing the length of the short url until a new url is found.
* **Error Handling** - Currently very basic error handling is implemented, there is a small easter egg when a short url can't be found when redirecting. In a real environment this would be replaced with an actual 404 page.
* **Security** - In a production environment a real key should be used with environment variables.
* **Faux Frontend** - In Lieu of a front end environment, I simply provided a swagger page. Via this page the APIs can be used.
* **Testing** - A full test suite is included, given more time I would add some more comprehensive integration tests. 

## Potential Enhancements
* **Caching** - Implementation of caching frequently used URLs.
* **Monitoring** - A more comprehensive monitoring of URLs to include detailed statistics such as geolocation.
* **Authentication** - User accounts and API key authentication, allowing private urls and also custom domains.
