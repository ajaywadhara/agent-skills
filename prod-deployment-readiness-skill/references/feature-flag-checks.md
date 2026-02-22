# Feature Flag Checks

Detailed patterns for detecting feature flag issues that cause unexpected behavior in production.

---

## Flag Framework Detection

### Java/Spring Boot

```java
// Spring Conditional
@ConditionalOnProperty(name = "feature.new-ui", havingValue = "true")

// Custom flag service
@Value("${feature.new-ui:false}")
private boolean newUiEnabled;

// LaunchDarkly
ldClient.boolVariation("new-ui-feature", user, false);

// Togglz
@FeatureToggle("NEW_UI")

// FF4J
ff4j.check("new-ui-feature")
```

### Node.js

```javascript
// Environment-based
process.env.FEATURE_NEW_UI === 'true'

// LaunchDarkly
ldClient.variation('new-ui-feature', user, false)

// Unleash
unleash.isEnabled('new-ui-feature')

// Custom config
config.features.newUi
features.isEnabled('new-ui')
```

### Python

```python
# Django Waffle
waffle.flag_is_active(request, 'new_ui')

# Environment-based
os.environ.get('FEATURE_NEW_UI', 'false') == 'true'

# LaunchDarkly
ld_client.variation('new-ui-feature', user, False)

# Django settings
settings.FEATURE_FLAGS.get('new_ui', False)
```

---

## Flag Lifecycle Analysis

### New Flag Detection

Search changed files for new flag references:

```regex
# Java
@ConditionalOnProperty\s*\(\s*name\s*=\s*"feature\.
@Value\s*\(\s*"\$\{feature\.
feature\.\w+[\.\w]*\s*[:=]

# Node.js
FEATURE_[A-Z_]+
features?\.(is)?[Ee]nabled\s*\(
\.variation\s*\(

# Python
FEATURE_[A-Z_]+
flag_is_active\s*\(.*,\s*['"]
```

### Changed Flag Detection

Detect when flag default values change:
- Config file shows `feature.x: false` changed to `feature.x: true`
- Code default changed: `getProperty("feature.x", false)` -> `getProperty("feature.x", true)`

### Removed Flag Detection

Detect when flags are removed from config but still referenced in code:
1. Find flags removed from config files (deleted lines in diff)
2. Search codebase for references to those flag names
3. Flag as WARNING if code references still exist

---

## Default State Validation

### Critical Rule: New Flags Should Default OFF in Production

| Scenario | Expected Default | Severity if Wrong |
|----------|-----------------|-------------------|
| New feature flag in prod config | `false` / OFF | BLOCKER |
| New feature flag with no prod config | Must have safe default in code | WARNING |
| Existing flag changed to ON in prod | Intentional? Verify | WARNING |
| Flag removed from prod config | Code must handle absence | WARNING |

### Detection Steps

1. Find new flag definitions in changed files
2. Check prod config (`application-prod.yml`, `.env.production`, etc.) for default value
3. Check code-level default (fallback value in `@Value`, `getProperty`, etc.)
4. If prod default is ON/true: BLOCKER
5. If no prod config exists and code default is ON/true: WARNING

---

## Dead Flag Detection

### Flags Removed from Config but Still in Code

```
# Detection workflow:
1. Find flags removed from config files (git diff shows deletion)
2. Extract flag names from deleted lines
3. Search entire codebase for those flag names
4. If found in code: WARNING (dead reference)
5. If not found in code: INFO (clean removal)
```

### Flags in Code but Not in Any Config

```
# Detection workflow:
1. Find all flag references in changed code
2. Check if corresponding config entry exists in any profile
3. If not: WARNING (orphaned flag, relies on code default only)
```

### Severity Rules

| Situation | Severity | Reason |
|-----------|----------|--------|
| Flag in code, removed from config | WARNING | Runtime error if code expects config |
| Flag in code, never in config | WARNING | Only code default applies |
| Flag in config, removed from code | INFO | Dead config, no runtime impact |
| Flag in both code and config, removed from both | INFO | Clean removal |

---

## Gradual Rollout Checklist

When new feature flags are detected, generate this checklist:

### Pre-Deployment
- [ ] Flag defaults to OFF in production
- [ ] Flag has a clear owner and description
- [ ] Rollout percentage plan documented (e.g., 1% -> 10% -> 50% -> 100%)
- [ ] Rollback mechanism tested (flag OFF disables feature completely)
- [ ] Metrics/monitoring tied to flag state

### During Rollout
- [ ] Error rates monitored per flag state
- [ ] Performance metrics compared (flag ON vs OFF)
- [ ] User feedback channel established
- [ ] Automatic rollback trigger defined (e.g., error rate > 5%)

### After Full Rollout
- [ ] Flag cleanup scheduled (remove flag, make feature permanent)
- [ ] Dead flag code removed within 2 sprint cycles
- [ ] Config entries cleaned up across all environments
