# Dependency Checks

Detailed patterns for detecting risky dependency changes before production deployment.

---

## Semver Analysis

### Version Bump Classification

| Bump Type | Example | Risk | Severity |
|-----------|---------|------|----------|
| Major (X.0.0) | 2.x -> 3.0.0 | Breaking API changes | WARNING |
| Minor (0.X.0) | 2.3 -> 2.4.0 | New features, possible behavior changes | INFO |
| Patch (0.0.X) | 2.3.1 -> 2.3.2 | Bug fixes only | INFO |
| Pre-release | 1.0.0-beta.1 | Unstable, not production-ready | BLOCKER |
| SNAPSHOT | 1.0.0-SNAPSHOT | Development version | BLOCKER |

### Detection Regex Per Package Manager

```regex
# Maven (pom.xml)
<version>[^<]*-SNAPSHOT</version>
<version>[^<]*-(alpha|beta|rc|RC|M\d+|CR\d+)[^<]*</version>

# Gradle (build.gradle, libs.versions.toml)
version\s*=\s*["'][^"']*-SNAPSHOT["']
version\s*=\s*["'][^"']*-(alpha|beta|rc|RC)[^"']*["']

# npm (package.json)
"[^"]+"\s*:\s*"[^"]*-(alpha|beta|rc|next|canary)[^"]*"

# Python (requirements.txt, pyproject.toml)
\w+==\d+\.\d+\.\d+(a|b|rc|dev)\d*
\w+.*\d+\.\d+\.\d+\.dev\d+
```

---

## Lock File Consistency Checks

### Per Stack

| Stack | Dependency File | Lock File | Check |
|-------|----------------|-----------|-------|
| Node.js (npm) | package.json | package-lock.json | Both must be in diff if either changed |
| Node.js (yarn) | package.json | yarn.lock | Both must be in diff if either changed |
| Node.js (pnpm) | package.json | pnpm-lock.yaml | Both must be in diff if either changed |
| Python (pip) | requirements.txt | requirements.txt (is lock) | N/A |
| Python (poetry) | pyproject.toml | poetry.lock | Both must be in diff if either changed |
| Python (pipenv) | Pipfile | Pipfile.lock | Both must be in diff if either changed |
| Java (Gradle) | build.gradle | gradle.lockfile (if used) | Check if lockfile is committed |
| Java (Maven) | pom.xml | N/A (resolved at build) | Check for version ranges |

### Detection Steps

1. Check if dependency manifest changed in diff
2. Check if corresponding lock file also changed
3. If manifest changed but lock file didn't: WARNING (lock file drift)
4. If lock file changed but manifest didn't: INFO (transitive update)

### Common Issues

| Issue | Severity | Description |
|-------|----------|-------------|
| package.json changed, no lock file update | WARNING | `npm install` not run, non-reproducible build |
| Lock file conflict markers | BLOCKER | Merge conflict in lock file |
| Lock file deleted | BLOCKER | Intentional? Completely non-reproducible builds |
| Version range in Maven (`[1.0,2.0)`) | WARNING | Non-deterministic builds |

---

## SNAPSHOT / Pre-Release / Beta Detection

### Files to Check

```
pom.xml
build.gradle / build.gradle.kts
gradle/libs.versions.toml
package.json
requirements.txt
pyproject.toml
Pipfile
```

### Patterns That Should Not Appear in Release

```regex
# Java/Maven/Gradle
-SNAPSHOT
-alpha
-beta
-RC\d+
-M\d+
-CR\d+
\.BUILD-SNAPSHOT

# Node.js
-alpha\.\d+
-beta\.\d+
-rc\.\d+
-next\.\d+
-canary

# Python
\.dev\d+
(a|b|rc)\d+
\.post\d+  # post-releases are usually fine but flag for awareness
```

### Severity
- BLOCKER: Any SNAPSHOT or pre-release dependency in a release branch/tag
- WARNING: Pre-release dependency in a feature branch targeting release

---

## Transitive Dependency Impact

### When to Check

Flag when a direct dependency has a major version bump, as it may pull in different transitive dependencies:

1. Identify major version bumps in changed dependency files
2. For each major bump, note potential transitive impact
3. Recommend running dependency tree analysis:

```bash
# Maven
mvn dependency:tree -Dincludes=groupId:artifactId

# Gradle
./gradlew dependencies --configuration runtimeClasspath

# npm
npm ls <package-name>

# pip
pip show <package-name>  # shows requires
pipdeptree -p <package-name>
```

### Severity Rules

| Situation | Severity | Action |
|-----------|----------|--------|
| Major version bump on core dependency | WARNING | Check changelog for breaking changes |
| Multiple major bumps in single release | WARNING | High risk of interaction issues |
| New dependency added | INFO | Review purpose and security |
| Dependency removed | INFO | Verify no runtime references remain |
| Transitive dependency conflict | WARNING | May cause classpath/module issues |

---

## New Dependency Review Checklist

When a new dependency is added to the project:

- [ ] Purpose documented (why is this needed?)
- [ ] License compatible with project license
- [ ] Actively maintained (last commit < 6 months)
- [ ] No known critical CVEs
- [ ] Size is reasonable (not pulling in unnecessary transitive deps)
- [ ] Not duplicating existing functionality in the project
