#! python
#
# http-tx.py
# Create continuous HTTP requests to a specified socket.
import argparse
import logging
import requests
import time
from urllib.parse import urlparse


# Set up logging configuration to log to a file and the console
# Create a logger
logger = logging.getLogger(__name__)
# File handler setup
file_handler = logging.FileHandler('http_tx.log')
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


def validate_url(url):
    try:
        parsed_url = urlparse(url)

        # Verify that the schemed defined is for http traffic
        if parsed_url.scheme not in ("http", "https"):
            raise argparse.ArgumentTypeError(
                f"Unaccepted URL scheme used - {parsed_url.scheme}"
            )

        # Verify netloc is a domain or IP
        if not parsed_url.netloc:
            raise argparse.ArgumentTypeError(
                f"Unaccepted network location - {parsed_url.netloc}"
            )

        return url

    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Error validating url - {url}"
        )


def send_http_req(url, method, file_path=None):
    logger.info(f"Sending {method} request to {url}")
    if file_path:
        try:
            # Open file in binary mode for reading
            with open(file_path, "rb") as file:
                attachment = {"file": (file_path, file)}
                # Send POST request
                response = requests.request(method, url, files=attachment, data=payload)
        except FileNotFoundError:
            logger.critical(f"File not found: {file_path}")
            quit()
        except Exception as e:
            logger.critical(f"An error occurred: {str(e)}")
            quit()
    else:
        response = requests.request(method, url)
    if 200 <= response.status_code < 300:
        logger.info(f"SUCCESS, received status code {response.status_code}")
        return
    else:
        logger.warning(f"FAIL, status code {response.status_code}")
        return


def main():
    parser = argparse.ArgumentParser(
        description="Continuous transmission of HTTP requests to specified host.",
        epilog="Use Ctrl+c to end transmission.",
        prog="http-tx.py",
    )

    parser.add_argument(
        "-t, --target",
        dest="target",
        help="URL to target with HTTP traffic (e.g., http://127.0.0.1:8080/)",
        metavar="Target",
        required=True,
        type=validate_url
    )

    parser.add_argument(
        "-p, --httpreq",
        default="get",
        dest="httpreq",
        help="HTTP request type, e.g., GET. Defaults to GET",
        metavar="HTTP_Request_Type",
        type=str,
    )

    parser.add_argument(
        "-f, --filepath",
        default=None,
        dest="filepath",
        help="Payload to send to server in HTTP POST request",
        metavar="File_path",
        type=str,
    )

    parser.add_argument(
        "-r, --reqpersec",
        default=1.0,
        dest="rps",
        help="Number of requests to make of the target per second, e.g., 1.0.",
        metavar="Requests_per_Second",
        type=float,
    )

    args = parser.parse_args()

    tx_delay = 1 / args.rps
    req_type = args.httpreq.upper()

    logger.info(f"Beginning HTTP {req_type} requests to {args.target}")

    try:
        while True:
            send_http_req(args.target, req_type)

            # Wait for the specified interval before sending the next request
            time.sleep(tx_delay)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Shutting down...")


if __name__ == "__main__":
    logger.debug(f"Running {__name__}...\n")
    main()
