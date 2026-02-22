# Stack-Specific Patterns

Detection rules and deployment patterns for each supported technology stack.

---

## Java / Spring Boot

### Stack Detection

```
# Files that indicate Java/Spring Boot:
pom.xml
build.gradle / build.gradle.kts
gradle/libs.versions.toml
src/main/java/**/*.java
application.yml / application.yaml / application.properties
```

### Configuration Files

| File | Purpose | Deployment Impact |
|------|---------|-------------------|
| `application.yml` | Main config | All environments |
| `application-{profile}.yml` | Profile-specific | Target environment only |
| `bootstrap.yml` | Early startup config | Config server, vault |
| `logback-spring.xml` | Logging config | Log routing, volume |
| `META-INF/spring.factories` | Auto-config | Bean loading |
| `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` | Boot 3+ auto-config | Bean loading |

### Spring-Specific Deployment Checks

| Check | Files | Pattern |
|-------|-------|---------|
| Profile activation | `application*.yml` | `spring.profiles.active` value |
| Actuator exposure | `application*.yml` | `management.endpoints.web.exposure.include` |
| Flyway migration naming | `db/migration/V*` | `V{version}__{description}.sql` |
| JPA DDL-auto | `application*.yml` | `spring.jpa.hibernate.ddl-auto` (BLOCKER if `create` or `create-drop` in prod) |
| Server port | `application*.yml` | `server.port` change |
| Context path | `application*.yml` | `server.servlet.context-path` change |
| DataSource URL | `application*.yml` | `spring.datasource.url` |

### Spring Boot Actuator Checks

```yaml
# BLOCKER: All actuator endpoints exposed in prod
management.endpoints.web.exposure.include: "*"

# SAFE: Only health and info
management.endpoints.web.exposure.include: health,info

# WARNING: Sensitive endpoints exposed
management.endpoints.web.exposure.include: env,configprops,beans
```

### Build Tool Patterns

```groovy
// Gradle - check for version changes in
plugins {
    id 'org.springframework.boot' version '...'
}

// Version catalog (libs.versions.toml)
[versions]
spring-boot = "..."
```

```xml
<!-- Maven - check parent version -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>...</version>
</parent>
```

---

## Node.js

### Stack Detection

```
# Files that indicate Node.js:
package.json
package-lock.json / yarn.lock / pnpm-lock.yaml
tsconfig.json
*.ts / *.js / *.tsx / *.jsx
next.config.js / nuxt.config.ts
```

### Configuration Files

| File | Purpose | Deployment Impact |
|------|---------|-------------------|
| `package.json` (scripts) | Build/start commands | How the app runs |
| `.env` / `.env.production` | Environment config | Runtime behavior |
| `next.config.js` | Next.js config | SSR, routing, rewrites |
| `nuxt.config.ts` | Nuxt config | SSR, modules, routing |
| `ecosystem.config.js` | PM2 config | Process management |
| `Procfile` | Heroku/platform config | How the app starts |

### Node-Specific Deployment Checks

| Check | Files | Pattern |
|-------|-------|---------|
| Start script changed | `package.json` | `scripts.start` or `scripts.build` |
| Engine requirement changed | `package.json` | `engines.node` version |
| New postinstall script | `package.json` | `scripts.postinstall` (may run in prod) |
| Environment mode | `.env*` | `NODE_ENV` value |
| Port configuration | `.env*`, code | `PORT` env var |
| Express middleware order | `app.js/ts` | Middleware chain (order matters) |
| Prisma schema change | `prisma/schema.prisma` | `prisma generate` + `prisma migrate` needed |

### npm Scripts That Affect Deployment

```json
{
  "scripts": {
    "start": "...",          // How production runs
    "build": "...",          // How production builds
    "postinstall": "...",    // Runs after npm install (including prod)
    "prestart": "...",       // Runs before start
    "migrate": "...",        // Database migration command
    "seed": "..."            // Data seeding (WARNING if runs in prod)
  }
}
```

### Common Node.js Deployment Issues

| Issue | Detection | Severity |
|-------|-----------|----------|
| `devDependencies` used in prod code | Import from dev-only package | BLOCKER |
| Missing build step | `build` script changed/removed | WARNING |
| Wrong NODE_ENV | Not set to `production` | WARNING |
| Memory limits not set | No `--max-old-space-size` | INFO |
| Uncaught exception handler missing | No `process.on('uncaughtException')` | WARNING |

---

## Python

### Stack Detection

```
# Files that indicate Python:
requirements.txt / requirements-*.txt
pyproject.toml
Pipfile / Pipfile.lock
setup.py / setup.cfg
*.py
manage.py (Django)
alembic.ini / alembic/ (SQLAlchemy)
```

### Configuration Files

| File | Purpose | Deployment Impact |
|------|---------|-------------------|
| `requirements.txt` | Dependencies | All environments |
| `pyproject.toml` | Project config + deps | Build and runtime |
| `settings.py` (Django) | App config | All environments |
| `settings/{env}.py` | Env-specific config | Target environment |
| `alembic.ini` | Migration config | Database connection |
| `gunicorn.conf.py` | WSGI server config | Process management |
| `uvicorn` config | ASGI server config | Process management |
| `celery.py` | Task queue config | Background processing |

### Framework Detection

```python
# Django
from django.* import ...
INSTALLED_APPS = [...]
urlpatterns = [...]

# Flask
from flask import Flask
app = Flask(__name__)

# FastAPI
from fastapi import FastAPI
app = FastAPI()
```

### Python-Specific Deployment Checks

| Check | Files | Pattern |
|-------|-------|---------|
| Django DEBUG mode | `settings*.py` | `DEBUG = True` in prod (BLOCKER) |
| Django ALLOWED_HOSTS | `settings*.py` | `ALLOWED_HOSTS = ['*']` (BLOCKER) |
| Django SECRET_KEY | `settings*.py` | Hardcoded secret (BLOCKER) |
| WSGI/ASGI server config | `gunicorn.conf.py`, `Procfile` | Worker count, timeout |
| Alembic migration | `alembic/versions/` | New revision files |
| Django migration | `*/migrations/*.py` | New migration files |
| Celery task changes | `tasks.py`, `celery.py` | Task signature, queue routing |
| Static files | `collectstatic` command | Must run before deploy |

### Common Python Deployment Issues

| Issue | Detection | Severity |
|-------|-----------|----------|
| `DEBUG = True` in prod | Django settings | BLOCKER |
| `ALLOWED_HOSTS = ['*']` | Django settings | BLOCKER |
| Missing static file collection | No `collectstatic` in deploy | WARNING |
| Alembic head conflict | Multiple heads in migration chain | BLOCKER |
| Missing Celery worker restart | Task signature changed | WARNING |
| requirements.txt unpinned | `package>=1.0` without upper bound | WARNING |
