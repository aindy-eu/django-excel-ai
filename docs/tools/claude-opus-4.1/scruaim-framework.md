# SCRUAIM Framework - Story-Driven AI Development

## What is SCRUAIM?

SCRUAIM is a lightweight agile framework designed specifically for AI-assisted development. It provides structure and rigor to what could otherwise be chaotic AI interactions, ensuring systematic progress toward production-ready software.

### The Acronym

- **S**tory-driven development - Every feature starts as a user story
- **C**ollaborative with AI - Designed for human-AI partnership
- **R**apid iterations - Fast feedback loops with continuous delivery
- **U**ser-focused outcomes - Business value drives technical decisions
- **A**rchitecture-aware - Maintains system coherence across features
- **I**ncremental delivery - Build on solid foundations
- **M**etrics-driven - Measurable quality and progress

## Core Components

### 1. The Story Pipeline

Stories progress through a clear pipeline:

```
draft/ → todo/ → in-progress/ → done/
```

Each stage has specific criteria:

- **draft/**: Stories being refined, not ready for implementation
- **todo/**: Ready for implementation with all requirements clear
- **in-progress/**: Currently being worked on (limit 1-2)
- **done/**: Completed with all acceptance criteria met

### 2. User Story Template

Every story follows this comprehensive structure:

```markdown
# US-XXX: [Story Title]

## Story

As a [user type]
I want to [action/feature]
So that I can [business value]

## Background & Context

[Why this story exists, dependencies, constraints]

## Acceptance Criteria

- [ ] Specific, measurable requirement 1
- [ ] Specific, measurable requirement 2
      [Minimum 5 criteria]

## Technical Approach

1. Step-by-step implementation plan
2. Specific Django patterns to use
3. Architecture decisions

## Testing Requirements

### Unit Tests (minimum 5)

- [ ] Test model validation
- [ ] Test view permissions
      [Specific test cases]

### Integration Tests

- [ ] Test full user flow
- [ ] Test API endpoints

## Security Checklist

- [ ] Authentication required
- [ ] Input validation
- [ ] SQL injection prevention
      [7+ security items]

## Performance Criteria

- Response time < X seconds
- Query count < Y
- Memory usage < Z MB

## Documentation

- [ ] Code comments for complex logic
- [ ] API documentation
- [ ] User guide updates

## Definition of Done

- [ ] All acceptance criteria met
- [ ] All tests passing
- [ ] Security checklist complete
- [ ] Performance criteria met
- [ ] Code review approved
- [ ] Documentation updated
```

### 3. Story Review Checklist

A 175-line review checklist ensures quality:

```markdown
# STORY-REVIEW.md

## Story Quality (15 checks)

- Clear user value?
- Measurable criteria?
- Single responsibility?

## Technical Design (20 checks)

- Django best practices?
- Database design optimal?
- API patterns consistent?

## Testing (15 checks)

- Coverage > 70%?
- Edge cases covered?
- Performance tests?

## Security (10 checks)

- Authentication verified?
- Authorization checked?
- Input sanitization?

## Production Readiness (15 checks)

- Error handling?
- Logging appropriate?
- Monitoring enabled?
```

## How It Works in Practice

### Example: Excel Upload Feature (US-006)

This real story from the project demonstrates SCRUAIM in action:

#### Story Definition

```markdown
As a dashboard user
I want to upload and view Excel files
So that I can prepare them for AI validation
```

#### Acceptance Criteria (19 items)

- File upload with drag-and-drop
- File type validation (.xlsx, .xls only)
- Size limit enforcement (10MB)
- Preview of uploaded data
- Progress indicators
- Error handling with user feedback

#### Technical Approach

1. Create ExcelFile model with FileField
2. Implement UploadView with HTMX
3. Add Alpine.js drag-drop handler
4. Create preview template with data tables
5. Add background processing for large files

#### Testing Requirements (10+ tests)

- Test file upload validation
- Test size limits
- Test preview generation
- Test error conditions
- Test concurrent uploads
- Performance test with 10MB files

#### Outcome

- Implemented in 4-8 hours
- 15 tests written
- 100% acceptance criteria met
- Performance target achieved (< 3s processing)

## Benefits of SCRUAIM

### 1. Predictable Quality

Every story has the same rigorous requirements:

- Minimum 5 acceptance criteria
- Minimum 10 tests
- Security checklist mandatory
- Performance targets defined

### 2. Knowledge Accumulation

Stories reference previous work:

```markdown
## Dependencies

- Requires US-003 (User model)
- Builds on US-005 (File upload patterns)
```

### 3. Incremental Complexity

Stories build on each other:

1. US-006: Basic Excel upload
2. US-008: Add AI validation
3. US-009: Add batch processing
4. US-010: Add scheduling

### 4. Clear Communication

Stories serve as contracts between human and AI:

- Human defines business value
- AI implements technical solution
- Both verify acceptance criteria

## Django-Specific Adaptations

SCRUAIM includes Django-specific patterns:

### Model Stories

```markdown
## Technical Approach

1. Create model in apps/[app]/models.py
2. Add admin registration
3. Create and run migrations
4. Add factory for testing
```

### View Stories

```markdown
## Technical Approach

1. Create CBV in views.py
2. Add URL pattern
3. Create template in app/templates/app/
4. Add LoginRequiredMixin
5. Implement get_queryset optimization
```

### API Stories

```markdown
## Technical Approach

1. Create ViewSet/APIView
2. Add serializer with validation
3. Configure URL router
4. Add permission classes
5. Implement pagination
```

## Integration with Other Tools

### With AI Handovers

Stories referenced in handovers:

```markdown
## Current State

- US-006: ✅ Completed
- US-008: 🔄 In Progress (validation endpoint done)
- US-009: 📋 Todo
```

### With Slash Commands

Stories verified through analysis:

```markdown
## Story Verification

US-006 claims: 10 tests, < 3s performance
Actual: 15 tests ✅, 2.3s average ✅
```

## Best Practices

### 1. One Story, One Purpose

Bad:

```
"User management and reporting system"
```

Good:

```
"User profile editing"
"User activity reports"
```

### 2. Measurable Criteria

Bad:

```
"System should be fast"
```

Good:

```
"Page load < 2 seconds for 100 records"
```

### 3. Comprehensive Testing

Bad:

```
"Add tests"
```

Good:

```
- [ ] Test valid file upload
- [ ] Test invalid file types
- [ ] Test oversized files
- [ ] Test concurrent uploads
```

### 4. Security First

Every story includes:

- Authentication requirements
- Authorization rules
- Input validation
- Output sanitization

## Metrics and Outcomes

Using SCRUAIM on this project produced:

- **7 stories completed** in 6 sessions
- **86% test coverage** (target was 70%)
- **60+ tests** written
- **Zero security issues** in production
- **100% acceptance criteria** met
- **2,500 lines** of quality code

## When to Use SCRUAIM

### Perfect For

- New feature development
- Systematic refactoring
- API development
- Bug fixing with reproduction
- Performance optimization

### Not Needed For

- Hotfixes
- Documentation updates
- Configuration changes
- Simple dependency updates

## Getting Started with SCRUAIM

### 1. Create Your First Story

```bash
# Create draft story
touch .claude/scruaim/user-stories/draft/US-XXX-feature-name.md

# Use template from user-stories/README.md
# Review against STORY-REVIEW.md

# Move to todo when ready
mv .claude/scruaim/user-stories/draft/US-XXX-*.md \
   .claude/scruaim/user-stories/todo/
```

### 2. Implement the Story

1. AI reads story from todo/
2. Creates implementation plan
3. Writes code following approach
4. Runs tests to verify
5. Checks acceptance criteria

### 3. Complete the Story

```bash
# Move to done
mv .claude/scruaim/user-stories/todo/US-XXX-*.md \
   .claude/scruaim/user-stories/done/

# Update backlog
echo "- US-XXX: Feature name ✅" >> .claude/scruaim/backlog/completed.md
```

## The SCRUAIM Philosophy

### Quality Through Structure

The framework proves that rigorous structure enables, rather than hinders, rapid development. By defining clear requirements upfront, implementation becomes straightforward.

### Collaborative Intelligence

SCRUAIM acknowledges that humans excel at defining business value while AI excels at implementation. The framework maximizes both strengths.

### Evidence-Based Progress

Every story completion is verifiable through tests, metrics, and acceptance criteria. Progress is measurable, not subjective.

## Conclusion

SCRUAIM transforms AI-assisted development from ad-hoc interactions into systematic software engineering. It provides the structure needed for AI to consistently deliver production-ready code while maintaining the flexibility needed for rapid iteration.

The framework's success on this Django project - delivering 7 complex features with 86% test coverage - demonstrates that AI can be a reliable partner in professional software development when given proper structure and clear requirements.
