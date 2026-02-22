# Configuration & Environment Checks

Detailed patterns for detecting configuration and environment issues that cause production incidents.

---

## Environment Variable Detection

### Java/Spring Boot
```
# Patterns to search for new env var references
@Value("${...}")
@ConfigurationProperties(prefix = "...")
System.getenv("...")
environment.getProperty("...")

# Config files
application.yml / application.yaml / application.properties
application-{profile}.yml
bootstrap.yml
```

### Node.js
```
process.env.VARIABLE_NAME
dotenv / .env / .env.production / .env.local
config.get('...')

# Config files
.env, .env.production, .env.staging, .env.development
config/*.json, config/*.js
```

### Python
```
os.environ["VARIABLE_NAME"]
os.environ.get("VARIABLE_NAME")
os.getenv("VARIABLE_NAME")
settings.VARIABLE_NAME (Django)

# Config files
.env, settings.py, config.py
pyproject.toml [tool.app.env]
```

---

## Environment Variable Analysis Workflow

1. **Find new env var references in changed code:**
   - Grep changed files for env var patterns per stack
   - Extract variable names

2. **Check if variables exist in deployment config:**
   - Search `docker-compose*.yml` for `environment:` section
   - Search `k8s/` or `kubernetes/` for ConfigMap/Secret definitions
   - Search `.env.example` or `.env.template`
   - Search Terraform `*.tf` files for variable definitions
   - Search CI/CD pipeline files for env declarations

3. **Flag missing variables:**
   - BLOCKER: Variable referenced in code but not found in any deployment config
   - WARNING: Variable in dev config but missing from prod config

---

## Profile/Environment Parity Checks

### Detect Config Drift

Compare configuration across environments:

```
# Java/Spring Boot - check parity across profiles
application.yml         (default)
application-dev.yml     (development)
application-staging.yml (staging)
application-prod.yml    (production)

# Key to check:
# - Properties present in dev but absent in prod
# - Different structure between profiles
# - Hardcoded dev URLs in non-dev profiles
```

### Parity Analysis Steps

1. List all config keys in changed profile files
2. Cross-reference against other profile files
3. Flag keys that exist in dev but not prod (WARNING)
4. Flag keys with dev-looking values in prod (BLOCKER: e.g., localhost, debug=true)

### Common Parity Issues

| Issue | Severity | Description |
|-------|----------|-------------|
| Property in dev, missing in prod | WARNING | May use default which could be wrong |
| `debug=true` in prod config | BLOCKER | Performance and security risk |
| `localhost` or `127.0.0.1` in prod | BLOCKER | Will fail in production |
| Log level set to DEBUG/TRACE in prod | WARNING | Performance and data exposure risk |
| Different database pool sizes without justification | INFO | May cause connection exhaustion |

---

## Secret Detection Patterns

### Regex Patterns for Common Secrets

```regex
# AWS
(AKIA[0-9A-Z]{16})
aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}

# API Keys / Tokens
(api[_-]?key|apikey|api[_-]?token)\s*[:=]\s*['"][A-Za-z0-9\-_.]{20,}['"]
(bearer|token|auth)\s*[:=]\s*['"][A-Za-z0-9\-_.]{20,}['"]

# Passwords / Connection Strings
(password|passwd|pwd)\s*[:=]\s*['"][^'"]{8,}['"]
(mysql|postgres|mongodb|redis):\/\/[^:]+:[^@]+@
jdbc:[a-z]+:\/\/.*password=[^&\s]+

# Private Keys
-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----
-----BEGIN OPENSSH PRIVATE KEY-----

# GitHub / GitLab Tokens
(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}
glpat-[A-Za-z0-9\-]{20,}

# Slack
xox[baprs]-[0-9a-zA-Z\-]{10,}

# Generic High-Entropy Strings (use with caution)
[A-Za-z0-9+/]{40,}={0,2}  # Base64 strings > 40 chars in config
```

### Files to Always Check for Secrets
- `*.yml`, `*.yaml`, `*.properties` (application config)
- `*.env`, `.env.*` (environment files)
- `docker-compose*.yml` (container config)
- `*.tf`, `*.tfvars` (Terraform)
- `**/k8s/**`, `**/kubernetes/**` (manifests)
- `Dockerfile*` (build args)

### Severity Rules
- BLOCKER: Any secret pattern matched in committed file
- BLOCKER: `.env` file with real values committed (not `.env.example`)
- WARNING: Secret reference without corresponding Vault/KMS/SecretManager setup
- INFO: New `@Value` or `process.env` reference (needs deployment config)

---

## Config Change Impact Matrix

| Change Type | Severity | Deployment Impact |
|-------------|----------|-------------------|
| New required env var | BLOCKER (if missing from deploy config) | App won't start |
| Default value changed | WARNING | Silent behavior change |
| Profile-specific override added | INFO | Only affects that environment |
| Database URL changed | BLOCKER (verify correctness) | Wrong DB = data corruption |
| Cache TTL changed | WARNING | Performance behavior change |
| Connection pool size changed | WARNING | Resource utilization change |
| Logging level changed | INFO | Observability impact |
| Feature toggle added | INFO | See Feature Flags category |
| Timeout value changed | WARNING | May affect SLAs |
| Retry config changed | WARNING | May cause cascading failures |

---

## New Config Without Documentation Detection

Flag when:
- New property added to `application*.yml` but no corresponding entry in README or docs
- New env var referenced but not in `.env.example` or `.env.template`
- New config class created (`@ConfigurationProperties`) without Javadoc or README update
- Severity: WARNING
