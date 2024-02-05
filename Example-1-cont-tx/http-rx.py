#! python
#
# http-python-examples/Example-1-cont-tx/http-rx.py
# A simple Python 3 server which listens on a specified IP address and port
# until a keyboard interrupt is sent.
import argparse
import http.server
import ipaddress
import logging
import socketserver


# Set up logging configuration to log to a file and the console
# Create a logger
logger = logging.getLogger(__name__)
# File handler setup
file_handler = logging.FileHandler('http_rx.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)

# Console handler setup
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s: %(message)s')
console_handler.setFormatter(console_formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Set the overall log level for the logger
logger.setLevel(logging.DEBUG)


def validate_ip_address(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return ip_str
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{ip_str} isn't a valid IP address..."
        )


# Define a custom request handler that logs requests
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Log the request with a timestamp
        logger.info("%s - %s" % (self.address_string(), format % args))
    
    def do_GET(self):
        # Handle GET requests
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, GET request!")

    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, POST request!")


def main():

    parser = argparse.ArgumentParser(
        description="HTTP listening process, python3 http-rx.py -p <port> -b <ip_addr>",
        epilog="Use Ctrl+c to end server process.",
        prog="http-tx.py",
    )

    parser.add_argument(
        "-p, --port",
        dest="port",
        help="Port to listen on (e.g., 8080)",
        metavar="bind_ip",
        required=True,
        type=int
    )

    parser.add_argument(
        "-b, --bind",
        default="0.0.0.0",
        dest="bind_ip",
        help="IP (of current machine) to listen on (e.g., 127.0.0.1, default 0.0.0.0)",
        metavar="bind_ip",
        type=validate_ip_address
    )

    args = parser.parse_args()

    try:
        # Create an HTTP server with the custom request handler
        with socketserver.TCPServer(("", args.port), RequestHandler) as httpd:
            logger.info(f"Server listening on port {args.port}")
            httpd.serve_forever()

    except KeyboardInterrupt:
        logger.info("Server stopped.")


if __name__ == "__main__":
    main()
