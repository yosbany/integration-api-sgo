# Zureo Integration API

A REST API for integrating with Zureo's inventory management system. This API provides endpoints for login, stock checking, and stock adjustment functionality.

## Features

- Login to Zureo system
- Check stock levels for specific SKUs
- Adjust stock levels for specific SKUs
- CORS enabled for cross-origin requests
- Environment variable configuration
- Health check endpoint

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your Zureo credentials:
```
ZUREO_CODIGO=your_company_code
ZUREO_EMAIL=your_email
ZUREO_PASSWORD=your_password
PORT=8000
```

## Running the API

Start the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /`
  - Returns API status and available endpoints

### Login
- `POST /zureo/login`
  - Body: `{"username": "your_email", "password": "your_password"}`
  - Returns login status

### Check Stock
- `GET /zureo/stock/{sku}`
  - Returns current stock level for the specified SKU

### Adjust Stock
- `GET /zureo/ajustar/{sku}/{cantidad}`
  - Adjusts stock level for the specified SKU to the given quantity

## Deployment to Render

1. Create a new Web Service on Render
2. Connect your repository
3. Set the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
4. Add your environment variables in the Render dashboard
5. Deploy!

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Security

- All sensitive data is stored in environment variables
- CORS is configured for security
- Session management is handled securely
- No sensitive data is logged

## License

MIT
