# Story Review Checklist - Django Excel AI Validator

> Use this checklist before moving stories from `draft/` to `todo/`

## Production Readiness Gate

### 0. Enterprise Standards
- [ ] **No Django Admin** usage in production code
- [ ] **Security first** - auth/permissions defined
- [ ] **PRM compliance** - no code duplication (2+ = component)
- [ ] **Performance budget** - queries/load time defined
- [ ] **Monitoring hooks** - what metrics to track

## Essential Checks

### 1. Story Completeness
- [ ] **User role** clearly defined (user, staff, admin, anonymous)
- [ ] **Action uses specific verbs** (upload, delete, view - not "manage")
- [ ] **Implementation details included** (drag-drop, file selection, etc.)
- [ ] **Business value** explicit in "so that" clause
- [ ] **Not a technical task** disguised as user story
- [ ] **References existing patterns** where applicable (e.g., "like email management")
- [ ] **Out of Scope section** included to prevent feature creep

### 2. Acceptance Criteria
- [ ] All criteria are **measurable** (not subjective)
- [ ] **User-visible behaviors** specified
- [ ] **UI interaction details** included (close buttons, cancel options)
- [ ] **Edge cases** considered
- [ ] **Error states** defined with specific messages
- [ ] **Success states** defined with feedback mechanism
- [ ] **File constraints** specified (size, type) if applicable
- [ ] Can be **tested** with pytest (tests in `apps/*/tests/`)

### 3. Technical Clarity

#### Django Components
- [ ] **Models**: Fields, relationships, and methods specified
- [ ] **Views**: CBV/FBV decision made, mixins identified
- [ ] **URLs**: Pattern and namespace defined
- [ ] **Templates**: Inheritance and blocks planned
- [ ] **Forms**: Fields and validation clear (if applicable)
- [ ] **Admin**: Registration needs identified

#### Database & Security
- [ ] **Migrations** impact understood
- [ ] **PostgreSQL features** utilized if beneficial
- [ ] **Indexes** considered for queries
- [ ] **Data integrity** rules defined
- [ ] **PII fields** identified for encryption
- [ ] **Audit requirements** specified
- [ ] **GDPR compliance** verified

#### Frontend
- [ ] **Template structure** follows project patterns
- [ ] **HTMX patterns** specified if using partial updates
- [ ] **Alpine.js components** planned if interactive
- [ ] **Dark mode support** considered
- [ ] **Tailwind utilities** identified (or custom CSS justified)
- [ ] **Responsive design** considered
- [ ] **JavaScript needs** documented (if any)
- [ ] **Loading/progress indicators** defined

### 4. Dependencies & Blockers
- [ ] **No unresolved dependencies**
- [ ] **Required packages** available in requirements.txt
- [ ] **No waiting on other stories** (or clearly noted)
- [ ] **Permissions/auth** requirements clear

### 5. Scope & Estimation
- [ ] **Single feature** (not multiple)
- [ ] **Completable in estimated time**
- [ ] **Not too large** (consider splitting if >8 hours)
- [ ] **Not too small** (batch if <1 hour)

## Django-Specific Checks

### Models & Database
- [ ] Field types use Django fields (CharField, TextField, etc.)
- [ ] Relationships properly defined (ForeignKey, ManyToMany)
- [ ] Model methods follow Django conventions
- [ ] Admin configuration appropriate for user needs
- [ ] Database constraints match business rules

### Views & URLs
- [ ] View class matches use case (TemplateView, ListView, CreateView, etc.)
- [ ] URL patterns follow project convention
- [ ] Namespace used consistently
- [ ] Login/permission requirements specified

### Templates
- [ ] Extends correct base template
- [ ] Uses project's component patterns
- [ ] Tailwind classes over custom CSS
- [ ] Forms use crispy_forms

### Security
- [ ] CSRF protection for forms
- [ ] Permission checks defined
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevention (template escaping)

## Quality Gates

### Code Quality
- [ ] Follows project's code style
- [ ] No code duplication planned
- [ ] Error handling specified
- [ ] Logging requirements noted

### User Experience
- [ ] Success messages defined
- [ ] Error messages user-friendly
- [ ] Loading states considered
- [ ] Accessibility basics covered

### Performance
- [ ] Database queries optimized (select_related, prefetch_related)
- [ ] Static files minimized
- [ ] Caching strategy noted (if needed)
- [ ] Pagination for large lists

## Red Flags 🚩

**Stop and reconsider if:**
- Story uses vague verbs like "manage", "handle", "process"
- Story contains "and" in the action (might be multiple stories)
- Technical implementation in user story format
- No clear user benefit
- Depends on undefined external systems
- Requires significant refactoring not mentioned
- "Nice to have" without clear value
- Performance requirements unrealistic
- Missing "Out of Scope" section (scope creep risk)
- No reference to existing patterns when similar features exist
- UI details incomplete (what happens on close? cancel? error?)
- File upload without size/type constraints specified

## Final Questions

Before approving:

1. **Would a new developer understand this story?**
2. **Can QA test this without asking questions?**
3. **Does this move the product forward?**
4. **Is this the simplest solution?**
5. **Will this integrate cleanly with existing code?**

## Approval Criteria

✅ **Ready for todo/** when:
- All essential checks pass
- No red flags present
- Questions have clear answers
- Implementation path is clear
- Estimate seems reasonable

❌ **Needs more work** when:
- Missing acceptance criteria
- Technical approach unclear
- Dependencies unresolved
- Scope too large/vague
- Security concerns unaddressed

## Notes for Reviewers

- **Be strict early**: Better to refine in draft than discover issues during implementation
- **Question complexity**: Can this be simpler?
- **Consider maintenance**: Will this create technical debt?
- **Think testing**: Write pytest tests in `apps/*/tests/` folders
- **Check patterns**: Does this match how we do things?

---

**Remember**: A well-reviewed story saves hours of implementation time and prevents costly rework.