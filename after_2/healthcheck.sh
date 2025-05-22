#!/bin/bash
set -e

# Check main page
curl -fs http://localhost:5000/ > /dev/null

# Check that /calculate does not leak env
RESPONSE1=$(curl -s "http://localhost:5000/calculate?expr=globals%28%29%5B%27PASSWORD%27%5D")
echo "$RESPONSE1" | grep -q '"error"' || exit 1

# Check that /ping does not allow command injection
RESPONSE2=$(curl -s "http://localhost:5000/ping?ip=127.0.0.1;%20cat%20/etc/passwd")
echo "$RESPONSE2" | grep -q '"error"' || exit 1