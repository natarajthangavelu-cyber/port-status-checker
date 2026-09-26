# Port Status Checker

A network socket utility in Python that checks open ports and service
responsiveness on a target host.

## Objective

Program network socket connections to audit open host ports.

## How it works

- Uses Python's built-in `socket` library (no external dependencies).
- Accepts a target IP/hostname and a port range as input.
- Attempts a TCP connect handshake on each port with a configurable timeout.
- Classifies each port as:
  - **Open** — handshake completed successfully.
  - **Closed** — connection actively refused.
  - **Filtered** — no response within the timeout (likely blocked by a firewall).
- Optionally grabs a service banner (e.g. HTTP/SSH greeting) for open ports.

## Requirements

- Python 3.x
- No external packages required.

## Usage

```bash
python3 port_status_checker.py
```

You'll be prompted for:
1. Target host (IP or hostname)
2. Port range (e.g. `20-100`)
3. Timeout in seconds (default `1.0`)
4. Whether to attempt banner grabbing on open ports

## Example

```
Enter target host (IP or hostname): scanme.nmap.org
Enter port range (e.g., 1-100): 20-100
Enter timeout in seconds (default 1.0): 1.0
Attempt to grab service banners for open ports? (y/n): y
```

## Important

Only scan hosts you own or have explicit permission to test.
`scanme.nmap.org` is a host maintained by the Nmap project specifically
for testing scanners like this one.

## Files

- `port_status_checker.py` — main script
- `execution_log.txt` — sample run output
