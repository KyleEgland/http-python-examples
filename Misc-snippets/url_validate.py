from urllib.parse import urlparse

def validate_url(url):
    try:
        parsed_url = urlparse(url)

        # Check if the scheme is either 'http' or 'https'
        if parsed_url.scheme not in ('http', 'https'):
            return False

        # Check if the network location (domain or IP) is valid
        if not parsed_url.netloc:
            return False

        # Check if the path is valid (optional)
        # In your case, you want to accept URLs with ports, so we don't specifically check the port here.
        # But you can add additional validation if needed.
        # For example, you can check that the port is a valid integer within a certain range.

        return True

    except ValueError:
        return False

# Test cases
valid_urls = [
    "http://example.com",
    "https://example.com",
    "http://127.0.0.1",
    "http://127.0.0.1:8080/",
    "https://127.0.0.1:8080/files/example.pdf",
]

invalid_urls = [
    "ftp://example.com",
    "http://",
    "https://",
    "http://127.0.0.1:",
    "http://example.com:abc",
    "http://example.com/path with spaces",
]

for url in valid_urls:
    if validate_url(url):
        print(f"'{url}' is a valid URL.")
    else:
        print(f"'{url}' is not a valid URL.")

for url in invalid_urls:
    if validate_url(url):
        print(f"'{url}' is a valid URL.")
    else:
        print(f"'{url}' is not a valid URL.")
