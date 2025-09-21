# User Story: CI/CD Pipeline Setup

**ID**: US-010
**Created**: 2025-09-20
**Status**: TODO
**Effort**: 4-6 hours
**Value**: High (Production Readiness)
**Risk**: Medium (External dependencies)

## Story

**As a** development team
**I want** automated CI/CD pipelines
**So that** code quality is maintained and deployments are reliable

## Background

This project currently has comprehensive testing (86% coverage) and code quality tools (black, ruff, mypy, bandit) configured locally. To be production-ready and maintainable as an open-source project, we need automated pipelines that run on every commit.

## Acceptance Criteria

- [ ] Tests run automatically on push and pull requests
- [ ] Code quality checks enforce standards
- [ ] Multiple Python versions tested (3.11, 3.12, 3.13)
- [ ] PostgreSQL service matches production setup
- [ ] Frontend assets build successfully
- [ ] Security vulnerabilities are detected
- [ ] Coverage reports are generated
- [ ] Build artifacts are created for deployment
- [ ] All checks must pass before merge

## Technical Design

### 1. GitHub Actions Structure

```
.github/
├── workflows/
│   ├── ci.yml          # Main CI pipeline
│   ├── deploy.yml      # Deployment workflow
│   └── security.yml    # Weekly security scan
└── dependabot.yml      # Automated dependency updates
```

### 2. CI Pipeline Jobs

#### Test Suite Job
- Matrix: Python 3.11, 3.12, 3.13
- PostgreSQL 16 service container
- Run pytest with coverage
- Upload coverage to CodeCov
- Fail if coverage < 70%

#### Code Quality Job
- Black formatting check
- Ruff linting
- MyPy type checking
- Bandit security linting
- djLint for templates

#### Frontend Build Job
- Node.js 20 setup
- Install npm dependencies
- Build Tailwind CSS
- Verify output exists

#### Pre-commit Job
- Run all pre-commit hooks
- Ensure consistency with local development

#### Security Scan Job
- Trivy filesystem scan
- Check for vulnerable dependencies
- Upload SARIF results

### 3. Deployment Pipeline

```yaml
# Triggers on main branch
# Runs tests first
# Builds production assets
# Creates deployment artifact
# Deploys to staging/production based on branch
```

### 4. Caching Strategy

- Python dependencies: `~/.cache/pip`
- Node modules: `node_modules`
- Build artifacts between jobs
- Cache key based on lock files

### 5. Environment Configuration

```yaml
env:
  PYTHON_VERSION: '3.13'
  NODE_VERSION: '20'
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  DATABASE_URL: postgres://...
```

## Implementation Notes

### Prerequisites
- GitHub repository
- Secrets configured in GitHub:
  - `CODECOV_TOKEN` (optional)
  - Production deployment secrets

### File: `.github/workflows/ci.yml`

Key sections to implement:

1. **Trigger Configuration**
   ```yaml
   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main]
   ```

2. **Service Containers**
   ```yaml
   services:
     postgres:
       image: postgres:16-alpine
       env:
         POSTGRES_PASSWORD: postgres
   ```

3. **Dependency Caching**
   ```yaml
   - uses: actions/cache@v4
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('requirements/*.lock') }}
   ```

4. **Test Execution**
   ```yaml
   - run: |
       pytest --cov=apps --cov-report=xml --cov-fail-under=70
   ```

### File: `.github/dependabot.yml`

Configure automated updates:
- Python packages (weekly)
- npm packages (weekly)
- GitHub Actions (weekly)
- Group related updates

## Testing Plan

1. **Local Validation**
   - Run `act` locally to test workflows
   - Verify all commands work in Docker

2. **Staged Rollout**
   - Enable on feature branch first
   - Test with intentional failures
   - Verify all error messages are clear

3. **Integration Testing**
   - Create test PR to trigger workflows
   - Verify matrix builds work
   - Check caching improves speed

## Success Metrics

- Build time < 5 minutes for average PR
- Zero false positives in linting
- Coverage maintained above 70%
- Security vulnerabilities detected before merge
- Deployment artifacts created successfully

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Flaky tests | High | Add retry logic, fix root causes |
| Slow builds | Medium | Optimize caching, parallelize jobs |
| PostgreSQL version mismatch | Low | Use same version as production |
| Action deprecation | Low | Dependabot updates, version pinning |

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Testing in Actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- Project's `.pre-commit-config.yaml` for tool versions
- `docs/testing/README.md` for test configuration

## Notes for Implementers

This story provides a production-ready CI/CD setup that:
- Matches the project's existing tool configuration
- Provides confidence in code quality
- Enables safe automated deployments
- Serves as a reference for Django projects

The implementation should take 4-6 hours for someone familiar with GitHub Actions, or 8-10 hours for someone learning the platform.

## Why This Matters

For an open-source project:
- **Trust**: Contributors see quality is enforced
- **Safety**: Changes can't break main branch
- **Efficiency**: No manual testing needed
- **Learning**: Clear example of modern DevOps

Even if not fully implemented, this story documents best practices and serves as a roadmap for production readiness.