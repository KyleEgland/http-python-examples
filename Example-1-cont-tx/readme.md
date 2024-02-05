# HTTPY Python Examples - Example 1, Continuous Transmission

Two programs to send (http-tx.py) and receive (http-rx.py) http traffic using Python 3.

## Quick Start

Start listener
`python3 http-rx.py -p <port> -b <ip_addr>`

Start sender
`python3 http-tx.py -t http://<ip_addr>:<port>` -h <http_req_type> -r <num_reqs_per_sec>`
