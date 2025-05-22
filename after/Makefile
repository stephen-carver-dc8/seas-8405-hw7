# Pre-build security checks
check:
	@echo "Running code analysis with Bandit..."
	@docker run --rm -v $(PWD):/app python:slim \
		sh -c "set -e && pip install --no-cache-dir bandit && bandit -r /app"; \
	BANDIT_EXIT=$$?; \
	echo "Running dependency check with pip-audit..."; \
	docker run --rm -v $(PWD):/app python:slim \
		sh -c "set -e && pip install --no-cache-dir pip-audit && pip-audit -r /app/requirements.txt"; \
	AUDIT_EXIT=$$?; \
	exit $$((BANDIT_EXIT || AUDIT_EXIT))

# Host security check
host-security:
	@echo "Running Docker Bench for Security..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security

# Build Docker image after security checks
dbuild: check
	docker build -t mywebapp .

# Scan the built image for vulnerabilities
scan:
	docker scout recommendations mywebapp_after:latest

# Docker Compose commands
build:
	docker compose build

start:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker system prune -f

reset: stop clean
	docker compose up -d --build

restart: stop start
