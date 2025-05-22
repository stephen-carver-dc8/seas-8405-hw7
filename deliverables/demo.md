1. cd before

1. app.py
    - Hardcoded secrets in PASSWORD variable. Never used. But still there.
    - Command injectoin with ping. Shell=true is bad practice. The IP input is not validated.
    - Calculate has an unsafe use of eval() that can lead to remote code execution and should use literal_eval or alternative.
    - Flask is running with unsafe defaults. The app should be limited to local host during development or behind a reverse proxy.

1. make start

curl -w "\n" http://localhost:15000/
curl -w "\n" http://localhost:15000/?name=Stephen
curl -w "\n" http://localhost:15000/ping?ip=8.8.8.8
curl -w "\n" "http://localhost:15000/ping?ip=127.0.0.1;%20cat%20/etc/passwd"
curl -w "\n" http://localhost:15000/calculate?expr=2%2B2
curl -w "\n" http://localhost:15000/calculate?expr=globals%28%29%5B%27PASSWORD%27%5D

make check

    This does not work as written. It only runs the first command. For now we will evaluate its output.

    We will now manually run the second command and evaluate its output.
    docker run --rm -v $(pwd):/app python:3.9-alpine sh -c "pip install pip-audit && pip-audit -r /app/requirements.txt"

make scan

make host-security

    These tools are not perfect. Notice it is warning about this file having incorrect ownership, when infact the ownership matches its expectations.

    [WARN] 3.15  - Ensure that Docker socket file ownership is set to root:docker
    [WARN]      * Wrong ownership for /var/run/docker.sock
    ls -al /var/run/docker.sock

cd ../after

app.py
    - Hardcoded secrets moved to ENV
    - Shell=true is bad practice and has been removed. Use the pydantic library to validate IP
    - Calculate has an unsafe use of eval() that can lead to remote code execution and should use literal_eval or alternative.
    - Flask is running with unsafe defaults. The app should be limited to local host during development or behind a reverse proxy.

Docerfile
    Use slim image
    Ensure curl and ping are available
    Ensure appuser
    Ensure port 5000
    Add health check

docker-compose.yaml
    Add `read_only`, `security_opt`, `mem_limit`, and `pids_limit`.
    Restrict port exposure to `127.0.0.1`.
    Use `.env` files for secret handling.

Makefile
    fix make check to allow non zero exits

make start

curl -w "\n" http://localhost:15001/

Must be done from inside container because of the flask restriction to local host

docker exec -it after-web-1 /bin/bash

curl -w "\n" http://localhost:5000/
curl -w "\n" http://localhost:5000/?name=Stephen
curl -w "\n" http://localhost:5000/ping?ip=8.8.8.8
curl -w "\n" "http://localhost:5000/ping?ip=127.0.0.1;%20cat%20/etc/passwd"
curl -w "\n" http://localhost:5000/calculate?expr=2%2B2
curl -w "\n" http://localhost:5000/calculate?expr=%222%2B2%22
curl -w "\n" http://localhost:5000/calculate?expr=globals%28%29%5B%27PASSWORD%27%5D

exit

make check

echo $?

make scan

make host-security

cd ../after2

make start

curl -w "\n" http://localhost:15002/
curl -w "\n" http://localhost:15002/?name=Stephen
curl -w "\n" http://localhost:15002/ping?ip=8.8.8.8
curl -w "\n" "http://localhost:15002/ping?ip=127.0.0.1;%20cat%20/etc/passwd"
curl -w "\n" http://localhost:15002/calculate?expr=2%2B2
curl -w "\n" http://localhost:15002/calculate?expr=globals%28%29%5B%27PASSWORD%27%5D

make check

echo $?

make scan

make host-security