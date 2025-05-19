
import os
import sys
import yaml
import json
from pathlib import Path

def update_dockerfile(dockerfile_path):
    content = dockerfile_path.read_text()
    modified = False

    if "USER appuser" not in content:
        if "RUN adduser" not in content:
            content += "\nRUN adduser --disabled-password --gecos '' appuser"
        content += "\nUSER appuser"
        modified = True

    if "HEALTHCHECK" not in content:
        content += """\n
# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:5000/ || exit 1
"""
        modified = True

    if modified:
        dockerfile_path.write_text(content)
        print(f"Updated {dockerfile_path}")
    else:
        print(f"No changes needed for {dockerfile_path}")

def update_compose(compose_path):
    content = compose_path.read_text()
    compose_data = yaml.safe_load(content)
    modified = False

    for service in compose_data.get('services', {}).values():
        if 'user' not in service:
            service['user'] = '1001:1001'
            modified = True
        if 'deploy' not in service:
            service['deploy'] = {}
        if 'resources' not in service['deploy']:
            service['deploy']['resources'] = {
                'limits': {
                    'cpus': '0.50',
                    'memory': '512M'
                },
                'reservations': {
                    'cpus': '0.25',
                    'memory': '256M'
                }
            }
            modified = True

    if modified:
        with open(compose_path, 'w') as f:
            yaml.dump(compose_data, f, default_flow_style=False)
        print(f"Updated {compose_path}")
    else:
        print(f"No changes needed for {compose_path}")

def update_daemon_json(path):
    default_config = {
        "icc": False,
        "userns-remap": "default",
        "no-new-privileges": True,
        "log-driver": "json-file",
        "log-opts": {
            "max-size": "10m",
            "max-file": "3"
        }
    }

    if path.exists():
        with open(path, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    else:
        config = {}

    updated = False
    for k, v in default_config.items():
        if config.get(k) != v:
            config[k] = v
            updated = True

    if updated:
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Updated {path}")
    else:
        print(f"No changes needed for {path}")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python docker_security_fixes.py <directory>")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    dockerfile_path = base_dir / "Dockerfile"
    compose_path = base_dir / "docker-compose.yml"
    daemon_path = base_dir / "daemon.json"

    update_dockerfile(dockerfile_path)
    update_compose(compose_path)
    update_daemon_json(daemon_path)
