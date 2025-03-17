def set_cors_headers(response):
    """Sets CORS headers in the response."""
    headers = {
        'Access-Control-Allow-Origin': '*',  # Replace with your domain for more security
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    response.headers.update(headers)
    return response
