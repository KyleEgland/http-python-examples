#! python
import argparse
import ipaddress


def validate_ip_address(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return ip_str
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{ip_str}' is not a valid IP address")


def main():
    parser = argparse.ArgumentParser(description="A program that accepts an IP address as an argument.")
    parser.add_argument("--ip", type=validate_ip_address, required=True, help="Specify an IP address")

    args = parser.parse_args()
    ip_address = args.ip

    print(f"Valid IP address provided: {ip_address}")


if __name__ == "__main__":
    main()
