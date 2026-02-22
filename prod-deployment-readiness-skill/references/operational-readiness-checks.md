# Operational Readiness Checks

Checklist-based checks for operational preparedness. These cannot be verified through code analysis alone — they require asking the deployer about processes and plans.

---

## Monitoring Checklist Templates

### By Change Type

#### New API Endpoint Added
- [ ] Endpoint latency metric configured (p50, p95, p99)
- [ ] Endpoint error rate metric configured (4xx, 5xx)
- [ ] Endpoint request volume metric configured
- [ ] Dashboard updated with new endpoint panel
- [ ] Alert rule for error rate > threshold

#### Database Migration
- [ ] Migration duration monitored
- [ ] Table lock duration monitored
- [ ] Query performance baseline captured before migration
- [ ] Slow query alerts configured
- [ ] Connection pool metrics monitored during migration
- [ ] Disk space alerts (migration may temporarily increase usage)

#### New External Integration
- [ ] External service latency metric configured
- [ ] Circuit breaker metrics configured
- [ ] External service error rate monitored
- [ ] Timeout alert configured
- [ ] Fallback behavior monitored

#### Infrastructure Change
- [ ] Resource utilization metrics (CPU, memory, disk) baselined
- [ ] Pod/container restart count monitored
- [ ] Health check status monitored
- [ ] Network latency between services monitored
- [ ] Auto-scaling metrics configured (if applicable)

#### Security Change
- [ ] Authentication success/failure rate monitored
- [ ] Authorization denial rate monitored
- [ ] Token expiration/renewal metrics
- [ ] Suspicious activity alerts configured

---

## Alert Rule Requirements

### Minimum Alerts for Any Deployment

| Alert | Threshold | Priority |
|-------|-----------|----------|
| Error rate (5xx) spike | > 5% of requests for 5 min | P1 - Critical |
| Latency degradation (p95) | > 2x baseline for 10 min | P2 - High |
| Pod/container crash loop | > 3 restarts in 10 min | P1 - Critical |
| Health check failure | Any pod unhealthy for 2 min | P1 - Critical |
| Memory usage | > 85% for 5 min | P2 - High |
| CPU usage | > 90% for 10 min | P2 - High |
| Disk usage | > 80% | P3 - Medium |
| External dependency failure | > 10% failure rate for 5 min | P2 - High |

### Alert Checklist for New Features

- [ ] Success metrics defined (how do we know the feature works?)
- [ ] Failure metrics defined (how do we know the feature is broken?)
- [ ] Alert thresholds set based on baseline (not arbitrary numbers)
- [ ] Alert routing configured (who gets paged?)
- [ ] Alert suppression during deployment window (if applicable)
- [ ] False positive mitigation (rate thresholds, not single events)

---

## Runbook Template

### Pre-Deploy Steps

```markdown
## Pre-Deploy Runbook: {Release Version}

### Prerequisites
- [ ] All CI/CD checks passing
- [ ] Staging environment validated
- [ ] Database backup completed (if migration included)
- [ ] Rollback version identified: {previous version/tag}
- [ ] Deployment window confirmed: {date/time}
- [ ] Stakeholders notified: {list}
- [ ] On-call engineer identified: {name}

### Environment Preparation
- [ ] Feature flags set to correct defaults
- [ ] New environment variables deployed to target environment
- [ ] New ConfigMaps/Secrets created in target cluster
- [ ] Database migration dry-run completed (if applicable)
- [ ] Infrastructure changes applied (Terraform, etc.)
```

### Deploy Steps

```markdown
### Deployment Steps

1. [ ] Start deployment monitoring dashboard
2. [ ] Initiate deployment to canary (if applicable)
3. [ ] Wait for canary health checks to pass ({N} minutes)
4. [ ] Monitor canary error rates for {N} minutes
5. [ ] If canary healthy, proceed to rolling deployment
6. [ ] Monitor rolling deployment progress
7. [ ] Verify all pods/instances healthy
8. [ ] Run smoke tests against production
```

### Post-Deploy Steps

```markdown
### Post-Deploy Verification

1. [ ] All health checks passing
2. [ ] Error rates at or below baseline
3. [ ] Latency at or below baseline
4. [ ] Smoke tests passing:
   - [ ] Critical path 1: {description}
   - [ ] Critical path 2: {description}
5. [ ] No new error patterns in logs
6. [ ] Feature flags verified (if applicable)
7. [ ] Database migration completed successfully (if applicable)
8. [ ] Downstream services unaffected

### Monitoring Window
- Duration: {30 minutes minimum}
- Metrics to watch: {error rate, latency, CPU, memory}
- Escalation: If any metric exceeds threshold, initiate rollback
```

---

## Rollback Plan Template

### Rollback Document

```markdown
## Rollback Plan: {Release Version}

### Rollback Trigger Conditions
Initiate rollback if ANY of the following occur:
- [ ] Error rate > {threshold}% for > 5 minutes
- [ ] p95 latency > {threshold}ms for > 10 minutes
- [ ] Health checks failing for > 2 minutes
- [ ] Critical business flow broken
- [ ] Data corruption detected

### Rollback Steps
1. [ ] Announce rollback in {#channel}
2. [ ] {Specific rollback command or process}
   - Option A: Revert to previous container image: {tag}
   - Option B: Revert git commit and redeploy
   - Option C: Feature flag OFF to disable change
3. [ ] Verify rollback deployed
4. [ ] Verify health checks passing
5. [ ] Verify error rates returning to baseline
6. [ ] Run smoke tests

### Database Rollback (if applicable)
- [ ] Rollback migration available: {yes/no}
- [ ] Rollback migration tested: {yes/no}
- [ ] Estimated rollback duration: {time}
- [ ] Data loss risk: {none/partial/full}
- [ ] Rollback command: {command}

### Rollback Timeline
- Decision to rollback: < 5 minutes after trigger
- Rollback execution: < {N} minutes
- Verification: < 10 minutes
- Total recovery time: < {N} minutes

### Post-Rollback
- [ ] Root cause investigation initiated
- [ ] Incident report drafted
- [ ] Fix planned before next deployment attempt
```

---

## Deployment Window Considerations

### Questions to Ask

| Question | Why It Matters |
|----------|---------------|
| When is the deployment window? | Avoid peak traffic hours |
| Is this a business-critical period? | Holiday freeze, month-end, etc. |
| What timezone are most users in? | Deploy during off-peak |
| Are other teams deploying simultaneously? | Coordinate to isolate issues |
| Is there a release freeze? | Respect organizational policies |
| Who is on-call during deployment? | Ensure support availability |

---

## Canary / Blue-Green / Rolling Guidance

### When to Use Each Strategy

| Strategy | Best For | Risk Level |
|----------|----------|------------|
| **Canary** | Database migrations, API changes, high-risk deploys | Low (small blast radius) |
| **Blue-Green** | Major version upgrades, infrastructure changes | Medium (full copy needed) |
| **Rolling** | Routine deployments, minor changes | Medium (gradual rollout) |
| **Feature Flag** | New features, A/B tests | Low (instant rollback) |

### Canary Deployment Checklist
- [ ] Canary percentage set: {1-10% recommended}
- [ ] Canary duration: {15-30 minutes recommended}
- [ ] Comparison metrics defined (canary vs baseline)
- [ ] Automatic rollback trigger configured
- [ ] Manual promotion gate after canary period
