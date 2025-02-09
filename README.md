# Online Products Store

## Prerequisites
Ensure you have the following installed:
- Python (>= 3.10)
- pip
- virtualenv (optional but recommended)
- sqlite3

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/tejas-21sept/DRF-APis-for-storing-production-with-user-authentication-mechanism.git
cd <project directory>
```

### 2. Create and Activate Virtual Environment
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root and add necessary configurations:
```
SECRET_KEY=your_secret_key
DEBUG=True
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Run the Server
```bash
python manage.py runserver
```

## API Endpoints
You can access the API using:
```
POST - http://127.0.0.1:8000/users/register/
POST - http://127.0.0.1:8000/users/login/
POST - http://127.0.0.1:8000/users/logout/
GET - http://127.0.0.1:8000/products/products/
POST - http://127.0.0.1:8000/products/products/
PUT - http://127.0.0.1:8000/products/products/<product_id>/
PATCH - http://127.0.0.1:8000/products/products/<product_id>/
DELETE - http://127.0.0.1:8000/products/products/<product_id>
POST - http://127.0.0.1:8000/products/products/<product_id>/disable
POST - http://127.0.0.1:8000/products/products/<product_id>/restore
GET - http://127.0.0.1:8000/products/export/

```
### Running Celery (If applicable)
```bash
celery -A project_name worker --loglevel=info
```


## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature-branch`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

