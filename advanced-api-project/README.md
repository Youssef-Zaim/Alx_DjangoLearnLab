## Filtering, Searching, and Ordering

### Filtering (django-filter)
- `?title=<substring>` — icontains on title
- `?author=<id>` — exact author id
- `?author_name=<substring>` — icontains on related Author.name
- `?publication_year=YYYY`
- `?year_min=YYYY&year_max=YYYY` — inclusive range on publication_year

### Search (SearchFilter)
- `?search=<text>` matches `title` and `author__name`.

### Ordering (OrderingFilter)
- `?ordering=<field>` or `?ordering=-<field>` for descending.
- Allowed: **any** model field (we set `ordering_fields = "__all__"`), e.g. `title`, `publication_year`, `id`.

**Examples**
