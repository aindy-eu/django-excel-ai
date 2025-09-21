# Rails to Django: A Developer's Journey

> A practical translation guide from a Rails developer who learned Django through building production features

## Why This Guide Exists

After years of Rails development, I was given a Django project with a cryptic hint: "take a look at Excel." This guide documents the mental model shifts, gotchas, and pleasant surprises I encountered building a production Django application with AI-powered Excel validation.

## Core Concept Mapping

### The Big Picture

| Rails Concept         | Django Equivalent | Key Differences                                  |
| --------------------- | ----------------- | ------------------------------------------------ |
| Rails app             | Django project    | Django "project" contains multiple "apps"        |
| Engine/Module         | Django app        | Apps are more isolated, explicit imports         |
| ActiveRecord          | Django ORM        | Similar query API, different relationship syntax |
| routes.rb             | urls.py + URLconf | More explicit, regex/path patterns               |
| ApplicationController | View mixins/CBVs  | Composition over inheritance                     |
| Action View           | Django Templates  | More explicit, less magic                        |
| Turbo/Stimulus        | HTMX/Alpine.js    | Same philosophy, different tools                 |

### Models & Database

| Rails                     | Django                            | Notes                                 |
| ------------------------- | --------------------------------- | ------------------------------------- |
| `has_many :posts`         | `post_set` (reverse FK)           | Django auto-creates reverse relations |
| `belongs_to :user`        | `ForeignKey(User)`                | Explicit field declaration            |
| `User.create!`            | `User.objects.create()`           | Manager pattern                       |
| `scope :published`        | `@classmethod` or Manager         | No built-in scope syntax              |
| `rails g model`           | `python manage.py makemigrations` | Two-step: make then migrate           |
| `schema.rb`               | Migration files                   | No single schema file                 |
| `find_by(email: x)`       | `filter(email=x).first()`         | `get()` raises exception if not found |
| `where.not(active: true)` | `exclude(active=True)`            | Different method name                 |
| `includes(:author)`       | `select_related('author')`        | Prevent N+1 queries                   |
| `includes(:comments)`     | `prefetch_related('comments')`    | For many-to-many/reverse FK           |

### Authentication

| Rails (Devise)                      | Django (Allauth)                | Notes                      |
| ----------------------------------- | ------------------------------- | -------------------------- |
| `current_user`                      | `request.user`                  | Attached to request        |
| `before_action :authenticate_user!` | `LoginRequiredMixin`            | Mixin for CBVs             |
| `user_signed_in?`                   | `request.user.is_authenticated` | Property, not method       |
| Built-in views                      | Customize templates             | Override allauth templates |

### Views & Controllers

| Rails           | Django                | Notes                   |
| --------------- | --------------------- | ----------------------- |
| Controller      | View                  | Naming swap!            |
| View (ERB)      | Template              | Django templates        |
| `respond_to`    | `if request.htmx`     | Content negotiation     |
| `before_action` | `dispatch()` override | Or use mixins           |
| `params[:id]`   | `self.kwargs['pk']`   | URL params in kwargs    |
| `render json:`  | `JsonResponse()`      | Explicit response types |

### Middleware

| Rails (Rack)            | Django Middleware    | Notes                     |
| ----------------------- | -------------------- | ------------------------- |
| `config.middleware.use` | `MIDDLEWARE` setting | Order matters             |
| `call(env)`             | `__call__(request)`  | Request/response pipeline |
| `before_action` in Rack | `process_request()`  | Pre-processing hook       |
| `after_action` in Rack  | `process_response()` | Post-processing hook      |

### Routing

```ruby
# Rails routes.rb
resources :posts do
  member do
    post :publish
  end
end
```

```python
# Django urls.py
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/publish/', PublishView.as_view(), name='post-publish'),
]
```

### Forms

| Rails             | Django         | Notes                         |
| ----------------- | -------------- | ----------------------------- |
| `form_for @post`  | `{{ form }}`   | Django forms handle rendering |
| Strong parameters | Forms validate | Validation in form layer      |
| `simple_form` gem | Crispy forms   | Similar form helpers          |

### Testing

| Rails (RSpec)      | Django (pytest)            | Notes                    |
| ------------------ | -------------------------- | ------------------------ |
| `let(:user)`       | `@pytest.fixture`          | Fixture pattern          |
| `before`           | `setup_method` / `setUp()` | pytest / Django TestCase |
| FactoryBot         | Factory Boy                | Same concept             |
| `expect().to eq()` | `assert x == y`            | Simpler assertions       |
| `rails_helper`     | `conftest.py`              | Shared config            |

## Gotchas That Got Me

### 1. No Built-in Authentication

Rails 8 has built-in authentication, Django has... nothing built-in. You need django-allauth or similar.

```python
# Don't forget to add to INSTALLED_APPS
'allauth',
'allauth.account',
'allauth.socialaccount',
```

### 2. Settings Split

Rails has one `application.rb`, Django splits settings:

```
config/
├── settings/
│   ├── base.py      # Shared settings
│   ├── development.py
│   ├── production.py
│   └── test.py
```

### 3. Apps Are More Isolated

In Rails, everything is autoloaded. In Django, explicit imports:

```python
# Must import from specific apps
from apps.users.models import User
from apps.excel_manager.views import ExcelListView
```

### 4. Templates Feel Verbose

Rails ERB is terse, Django is explicit:

```erb
<!-- Rails -->
<%= link_to "Edit", edit_post_path(post) %>
```

```django
<!-- Django -->
<a href="{% url 'post-edit' post.pk %}">Edit</a>
```

### 5. URL Reversing

Rails has path helpers, Django uses names:

```python
# In views
reverse('post-detail', kwargs={'pk': post.pk})

# In templates
{% url 'post-detail' post.pk %}
```

### 6. Migrations Are Manual

No `rails g model` magic:

```bash
# After changing models
python manage.py makemigrations
python manage.py migrate
```

### 7. Static Files Complexity

Rails asset pipeline vs Django's static files:

```python
# Development: served by Django
STATIC_URL = '/static/'

# Production: collect to STATIC_ROOT
python manage.py collectstatic

# Most projects use WhiteNoise for production serving
# pip install whitenoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]
```

## Pleasant Surprises

### 1. Admin Interface

Django's admin is incredible out of the box:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
```

### 2. Management Commands

Like rake tasks but cleaner:

```python
# apps/core/management/commands/import_data.py
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Your logic here
```

### 3. Class-Based Views

More reusable than Rails controllers:

```python
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 20
    # That's it! Template, context, pagination handled
```

### 4. QuerySet API

Chainable like ActiveRecord but more explicit:

```python
Post.objects.filter(
    status='published'
).select_related(
    'author'
).prefetch_related(
    'comments'
).order_by('-created_at')[:10]
```

### 5. Template Inheritance

Better than Rails layouts:

```django
<!-- base.html -->
{% block content %}{% endblock %}

<!-- child.html -->
{% extends "base.html" %}
{% block content %}
    <!-- Your content -->
{% endblock %}
```

## Dependency Management

| Rails          | Django                | Purpose                     |
| -------------- | --------------------- | --------------------------- |
| Gemfile        | requirements.txt      | Dependencies list           |
| Gemfile.lock   | requirements.lock     | Locked versions (pip-tools) |
| bundle install | pip install -r        | Install dependencies        |
| bundle update  | pip-compile --upgrade | Update dependencies         |

```bash
# Django with pip-tools (similar to Bundler)
pip-compile requirements/base.txt -o requirements/base.lock
pip-sync requirements/base.lock
```

## Code Quality Tools

| Rails     | Django       | Purpose              |
| --------- | ------------ | -------------------- |
| RuboCop   | Ruff/Black   | Linting & formatting |
| Reek      | pylint       | Code smells          |
| SimpleCov | coverage.py  | Test coverage        |
| Guard     | pytest-watch | Auto-run tests       |

## Project Structure Comparison

```
# Rails
app/
├── controllers/
├── models/
├── views/
└── assets/

# Django
apps/
├── users/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/users/
├── posts/
│   ├── models.py
│   ├── views.py
│   └── templates/posts/
```

## The HTMX/Alpine.js Stack

Coming from Rails Turbo/Stimulus, HTMX/Alpine.js feels familiar:

| Turbo               | HTMX        | Purpose         |
| ------------------- | ----------- | --------------- |
| `data-turbo-frame`  | `hx-target` | Target element  |
| `data-turbo-stream` | `hx-swap`   | How to update   |
| Turbo Drive         | `hx-boost`  | Page navigation |

| Stimulus          | Alpine.js | Purpose            |
| ----------------- | --------- | ------------------ |
| `data-controller` | `x-data`  | Component state    |
| `data-action`     | `@click`  | Event handlers     |
| `data-target`     | `x-ref`   | Element references |

### WebSockets & Real-time

| Rails (ActionCable)  | Django (Channels) | Notes                        |
| -------------------- | ----------------- | ---------------------------- |
| `ActionCable.server` | `channels.layers` | Message broker               |
| `ApplicationCable`   | `Consumer` class  | WebSocket connection handler |
| `broadcast_to`       | `group_send()`    | Send to channel group        |
| `stream_from`        | `group_add()`     | Subscribe to channel         |
| Built into Rails     | Separate package  | `pip install channels`       |

## Key Mindset Shifts

### 1. Explicit > Implicit

Django favors explicit imports and configuration. No autoloading magic.

### 2. Composition > Inheritance

Use mixins and composition rather than deep inheritance hierarchies.

### 3. Apps Are Boundaries

Think of apps as bounded contexts. Keep them focused.

### 4. Templates Are Logic-Light

Business logic belongs in views/models, not templates.

### 5. Settings Are Environment-Specific

Embrace the base/dev/prod split. It's cleaner long-term.

## My Favorite Django Features

1. **Admin Interface** - Saves weeks of development
2. **ORM Prefetching** - `select_related` and `prefetch_related` are powerful
3. **Management Commands** - Cleaner than rake tasks
4. **Middleware** - Request/response pipeline is elegant
5. **Template Inheritance** - Multiple block inheritance is fantastic

## Resources That Helped

- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) - Best practices
- [Django documentation](https://docs.djangoproject.com/) - Exceptionally well-written
- [Classy Class-Based Views](https://ccbv.co.uk/) - CBV reference
- [Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar) - Essential for development

## Final Thoughts

Django feels more explicit and "batteries included" than Rails. While Rails optimizes for developer happiness with conventions, Django optimizes for clarity and explicitness. Both are excellent frameworks - Django just requires a slight mental model adjustment.

The journey from Rails to Django taught me to appreciate both ecosystems. Django's explicit nature initially felt verbose, but it makes large codebases more maintainable. The admin interface alone justifies learning Django.

---

_Written for Rails developers discovering Django's way through building production features_
