# Infrastructure Checks

Detailed patterns for detecting infrastructure changes that affect deployment safety.

---

## Dockerfile Analysis

### Patterns to Check

| Pattern | Severity | Description |
|---------|----------|-------------|
| `FROM` tag changed | WARNING | Different base OS, libraries, behavior |
| `FROM` using `latest` tag | WARNING | Non-reproducible builds |
| `FROM` image removed (multi-stage) | BLOCKER | Build will fail |
| `ENV` added/changed | INFO | Environment behavior change |
| `EXPOSE` port changed | WARNING | Network/firewall rules may need updating |
| `HEALTHCHECK` removed | BLOCKER | Container orchestrator loses health visibility |
| `HEALTHCHECK` path changed | WARNING | Must match application health endpoint |
| `USER` directive removed | WARNING | Container may run as root |
| `COPY`/`ADD` paths changed | WARNING | Files may not be available at runtime |
| Build arg (`ARG`) added without default | WARNING | Build may fail without explicit value |

### Detection Regex

```regex
# Base image change
^-FROM\s+.+
^+FROM\s+.+

# Exposed ports
^[+-]EXPOSE\s+\d+

# Health check
^-HEALTHCHECK\s+
^+HEALTHCHECK\s+NONE

# Environment variables
^[+-]ENV\s+

# User directive
^-USER\s+
```

### Dockerfile Best Practices Check

When Dockerfile is changed, verify:
- [ ] Multi-stage build used (not copying build tools to runtime)
- [ ] Non-root user specified (`USER` directive)
- [ ] `HEALTHCHECK` defined
- [ ] Specific image tags used (not `latest`)
- [ ] `.dockerignore` exists and is appropriate
- [ ] No secrets in build args or environment

---

## Kubernetes Manifest Checks

### Critical Patterns

| Pattern | Severity | Description |
|---------|----------|-------------|
| Resource limits removed | BLOCKER | OOM kills, noisy neighbor |
| Resource limits drastically reduced | WARNING | May cause throttling |
| Readiness probe removed | BLOCKER | K8s routes traffic to unready pods |
| Liveness probe removed | BLOCKER | Stuck pods won't be restarted |
| Probe path changed | WARNING | Must match application endpoint |
| Replica count changed | WARNING | Capacity/cost impact |
| ConfigMap/Secret reference changed | WARNING | Must exist in target cluster |
| New ConfigMap/Secret referenced | WARNING | Must be created before deployment |
| Image pull policy changed | WARNING | May pull stale images |
| Service port changed | WARNING | Ingress/load balancer rules may break |
| PVC/storage changes | WARNING | Data persistence impact |
| Node selector/affinity changed | WARNING | Scheduling impact |

### Detection in K8s Manifests

```yaml
# Files to check
**/k8s/**/*.yml
**/k8s/**/*.yaml
**/kubernetes/**/*.yml
**/helm/**/*.yaml
**/helm/**/values*.yaml
**/charts/**/*.yaml
kustomization.yaml

# Patterns to detect
resources:
  limits:     # Check if removed or reduced
  requests:   # Check if removed or reduced

livenessProbe:   # Check if removed or path changed
readinessProbe:  # Check if removed or path changed
startupProbe:    # Check if removed or path changed

envFrom:
  - configMapRef:  # Check if reference exists
  - secretRef:     # Check if reference exists

env:
  - valueFrom:
      configMapKeyRef:  # Check if key exists
      secretKeyRef:     # Check if key exists
```

### Helm Values Changes

When `values.yaml` or environment-specific values change:
- WARNING: New value without default in template
- WARNING: Value type changed (string -> number, etc.)
- INFO: Value updated (e.g., replica count, image tag)

---

## Terraform / IaC Change Detection

### Files to Watch

```
*.tf
*.tfvars
*.tf.json
modules/**/*.tf
environments/**/*.tf
```

### Critical Patterns

| Pattern | Severity | Description |
|---------|----------|-------------|
| Resource deleted (`- resource "..."`) | BLOCKER | Infrastructure destruction |
| Security group rules changed | WARNING | Network access impact |
| IAM policy changed | WARNING | Permission changes |
| Instance type changed | WARNING | Capacity/cost impact |
| Database instance modified | WARNING | Possible downtime |
| Load balancer target changed | WARNING | Traffic routing impact |
| DNS record changed | WARNING | Service discovery impact |
| New provider added | INFO | New cloud service dependency |

### Terraform Plan Recommendation

When `.tf` files are changed:
```
RECOMMENDATION: Run `terraform plan` in a non-production environment
to verify the exact changes before applying to production.
```

---

## CI/CD Pipeline Change Analysis

### Files to Watch

```
.github/workflows/*.yml
.gitlab-ci.yml
Jenkinsfile
.circleci/config.yml
cloudbuild.yaml
bitbucket-pipelines.yml
.travis.yml
azure-pipelines.yml
```

### Critical Patterns

| Pattern | Severity | Description |
|---------|----------|-------------|
| Deploy step removed or commented out | BLOCKER | Deployment won't happen |
| Deploy target/environment changed | BLOCKER | May deploy to wrong environment |
| Approval/gate step removed | WARNING | Removes human verification |
| Secret reference changed/removed | WARNING | Pipeline may fail |
| New environment variable required | WARNING | Must be set in CI/CD |
| Test step removed | WARNING | Reduced quality gate |
| Build command changed | WARNING | Different build output |
| Artifact path changed | WARNING | Deployment may use wrong artifact |
| Trigger conditions changed | INFO | Different deployment triggers |

---

## Network Topology Changes

### Patterns That Affect Network

| Change | Severity | Required Action |
|--------|----------|-----------------|
| New external service URL | WARNING | Firewall/egress rules may need updating |
| New port exposed | WARNING | Security group/firewall rules |
| Protocol change (HTTP -> gRPC) | WARNING | Load balancer configuration |
| New domain/hostname | WARNING | DNS, TLS certificate |
| mTLS configuration added | WARNING | Certificate distribution |
| Service mesh config change | WARNING | Istio/Envoy routing impact |

### Detection Steps

1. Search changed files for new URLs, hostnames, ports
2. Check if corresponding infrastructure config updated
3. Flag missing infrastructure updates
