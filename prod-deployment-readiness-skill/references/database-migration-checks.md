# Database Migration Checks

Detailed patterns for detecting dangerous database migrations that cause downtime, data loss, or deployment failures.

---

## Migration Framework Detection

### Java/Spring Boot
```
# Flyway
src/main/resources/db/migration/V{version}__{description}.sql
src/main/resources/db/migration/R__{description}.sql (repeatable)
flyway.* properties in application.yml

# Liquibase
src/main/resources/db/changelog/*.xml|*.yaml|*.sql
spring.liquibase.* properties
```

### Node.js
```
# Prisma
prisma/migrations/{timestamp}_{name}/migration.sql
prisma/schema.prisma

# Knex
migrations/{timestamp}_{name}.js
knexfile.js

# TypeORM
src/migrations/{timestamp}-{name}.ts
```

### Python
```
# Alembic (SQLAlchemy)
alembic/versions/{revision}_{description}.py
alembic.ini

# Django
{app}/migrations/{number}_{name}.py
```

---

## Destructive Operation Patterns

### BLOCKER - Data Loss Risk

```sql
-- These patterns require expand-contract migration or explicit data preservation

DROP TABLE {table_name}
DROP COLUMN {column_name}
TRUNCATE TABLE {table_name}
DELETE FROM {table_name}  -- without WHERE or with broad WHERE
ALTER TABLE {table} DROP CONSTRAINT
ALTER TABLE {table} ALTER COLUMN {col} TYPE  -- type change may lose data
```

### Detection Regex

```regex
# SQL patterns (case-insensitive)
(?i)DROP\s+TABLE\s+
(?i)DROP\s+COLUMN\s+
(?i)ALTER\s+TABLE\s+\w+\s+DROP\s+
(?i)TRUNCATE\s+(TABLE\s+)?
(?i)DELETE\s+FROM\s+\w+\s*;       # DELETE without WHERE
(?i)ALTER\s+TABLE\s+\w+\s+ALTER\s+COLUMN\s+\w+\s+(SET\s+DATA\s+)?TYPE

# Liquibase XML
<dropTable\s
<dropColumn\s
<delete\s

# Alembic Python
op\.drop_table\(
op\.drop_column\(
op\.alter_column\(.*type_=
```

---

## Backward-Compatible Migration Patterns

### Expand-Contract Pattern (Recommended)

**Phase 1: Expand (safe to deploy)**
```sql
-- Add new column with default (backward-compatible)
ALTER TABLE users ADD COLUMN email_v2 VARCHAR(255) DEFAULT '';

-- Copy data in batches
UPDATE users SET email_v2 = email WHERE id BETWEEN ? AND ?;
```

**Phase 2: Migrate code (safe to deploy)**
- Update application to read/write new column
- Old column still exists, no data loss

**Phase 3: Contract (separate deployment)**
```sql
-- Remove old column after all code uses new one
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_v2 TO email;
```

### Safe Patterns to Encourage

| Operation | Safe Approach | Severity if Missing |
|-----------|--------------|---------------------|
| Add column | `ADD COLUMN ... DEFAULT ...` (with default) | INFO |
| Add column | `ADD COLUMN ... NULL` (nullable) | INFO |
| Rename column | Add new + copy + drop old (3 migrations) | WARNING if done in 1 step |
| Change type | Add new column, migrate data, drop old | BLOCKER if direct ALTER TYPE |
| Drop column | Verify no code references first | BLOCKER if still referenced |
| Drop table | Verify no foreign keys, no code references | BLOCKER if still referenced |
| Add index | `CREATE INDEX CONCURRENTLY` (Postgres) | WARNING if not concurrent |

---

## Migration Ordering Conflict Detection

### Flyway
```
# Check for duplicate version numbers
V1_001__create_users.sql
V1_001__create_orders.sql   <-- CONFLICT! Same version

# Check for gaps
V1_001, V1_002, V1_004      <-- V1_003 missing (WARNING)
```

### Detection Steps

1. List all migration files in changed set
2. Extract version numbers
3. Compare against existing migration versions
4. Flag duplicates (BLOCKER: will fail on deploy)
5. Flag gaps (WARNING: may indicate missing migration)

### Cross-Branch Conflicts

When multiple branches add migrations:
```
main:    V1_010__existing.sql
branch1: V1_011__feature_a.sql
branch2: V1_011__feature_b.sql  <-- Will conflict when both merge
```

- BLOCKER: Two migration files with same version number in diff
- WARNING: Migration version that may conflict with pending PRs (if detectable)

---

## Large Table Migration Safety

### Detection: Large Table Risk

Flag migrations that ALTER tables known to be large (or that match common large-table patterns):

```sql
-- Patterns that lock tables (problematic for large tables)
ALTER TABLE {large_table} ADD COLUMN ...       -- Without DEFAULT in older MySQL
ALTER TABLE {large_table} MODIFY COLUMN ...
ALTER TABLE {large_table} ADD INDEX ...
CREATE INDEX ON {large_table} ...              -- Without CONCURRENTLY

-- Safe alternatives
ALTER TABLE {table} ADD COLUMN ... DEFAULT ... -- Postgres 11+, MySQL 8.0+
CREATE INDEX CONCURRENTLY ...                  -- Postgres
ALTER TABLE ... ALGORITHM=INPLACE ...          -- MySQL Online DDL
pt-online-schema-change                        -- Percona toolkit
gh-ost                                         -- GitHub online schema migration
```

### Severity Rules for Large Table Operations

| Operation | Small Table (<1M rows) | Large Table (>1M rows) |
|-----------|----------------------|----------------------|
| ADD COLUMN (nullable) | INFO | WARNING |
| ADD COLUMN (with default) | INFO | WARNING (check DB version) |
| ADD INDEX | INFO | WARNING (use CONCURRENTLY) |
| DROP COLUMN | WARNING | BLOCKER (use expand-contract) |
| ALTER TYPE | WARNING | BLOCKER (use expand-contract) |
| ADD CONSTRAINT | INFO | BLOCKER (validate separately) |

---

## Entity/Model Change Without Migration Detection

### Java/Spring (JPA/Hibernate)

```java
// Detect @Entity changes without corresponding migration:
// 1. Find changed @Entity classes
// 2. Check if migration file also changed
// 3. Flag if entity changed but no migration added

@Entity
@Table(name = "users")
public class User {
    // New field added but no V{N}__add_field.sql
    private String newField;  // WARNING
}
```

### Detection Steps

1. Find changed files matching entity/model patterns:
   - Java: `@Entity`, `@Table` annotations
   - Node/Prisma: `prisma/schema.prisma` model changes
   - Python/Django: `models.py` changes
   - Python/SQLAlchemy: classes extending `Base`

2. Check if corresponding migration file exists in the same diff

3. Severity:
   - WARNING: Entity field added/removed without migration
   - WARNING: Entity relationship changed without migration
   - INFO: Entity annotation change (may be handled by Hibernate auto-DDL)

---

## Migration Rollback Verification

### Check for Rollback Support

| Framework | Rollback Mechanism | Check |
|-----------|-------------------|-------|
| Flyway | Undo migrations (`U{version}__*.sql`) | Look for corresponding U file |
| Liquibase | `rollback` section in changeset | Check each changeset has rollback |
| Alembic | `downgrade()` function | Verify non-empty downgrade in revision |
| Django | Django auto-generates reverse | Usually safe, check `RunSQL` has reverse |
| Prisma | No built-in rollback | WARNING: manual rollback needed |
| Knex | `down()` function | Verify non-empty down migration |

### Severity
- WARNING: Forward migration without rollback mechanism
- BLOCKER: Destructive forward migration without tested rollback
