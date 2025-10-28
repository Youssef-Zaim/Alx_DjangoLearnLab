# api/test_views.py
"""
Unit tests for Book API endpoints.

Covers:
- CRUD (create, retrieve, update, delete)
- Permissions (anonymous vs authenticated)
- Filtering (title, author, author_name, publication_year, ranges)
- Search (?search=)
- Ordering (?ordering=field / -field)

Run:  python manage.py test api
"""
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Author, Book


class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Users
        User = get_user_model()
        cls.user = User.objects.create_user(username="tester", password="pass1234")

        # Authors
        cls.author1 = Author.objects.create(name="Toni Morrison")
        cls.author2 = Author.objects.create(name="Chinua Achebe")

        # Books
        cls.book1 = Book.objects.create(
            title="Beloved", publication_year=1987, author=cls.author1
        )
        cls.book2 = Book.objects.create(
            title="Jazz", publication_year=1992, author=cls.author1
        )
        cls.book3 = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=cls.author2
        )

    def setUp(self):
        self.client = APIClient()

    # ---------- Helpers
    def _auth(self):
        """Authenticate the client as a valid user."""
        self.client.force_authenticate(user=self.user)
        
    def test_session_login_and_read_list(self):
        """Prove we can log in via session auth (uses the separate test DB)."""
        logged_in = self.client.login(username="tester", password="pass1234")
        self.assertTrue(logged_in)

        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Clean up session for isolation
        self.client.logout()    

    # ---------- Read: List & Detail
    def test_list_books_public(self):
        url = reverse("book-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.json()), 3)
        # Ensure expected keys exist
        first = resp.json()[0]
        for key in ("id", "title", "publication_year", "author"):
            self.assertIn(key, first)

    def test_detail_book_public(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data  # <- use DRF's parsed data
        self.assertEqual(data["id"], self.book1.id)
        self.assertEqual(data["title"], "Beloved")
        self.assertEqual(data["publication_year"], 1987)
        self.assertEqual(data["author"], self.author1.id)

    # ---------- Create
    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        payload = {"title": "Song of Solomon", "publication_year": 1977, "author": self.author1.id}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_success_and_future_year_validation(self):
        self._auth()
        url = reverse("book-create")

        # Valid create
        payload = {"title": "Song of Solomon", "publication_year": 1977, "author": self.author1.id}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # prove body shape using response.data
        self.assertEqual(response.data["title"], "Song of Solomon")

        # Invalid: future year
        future = date.today().year + 1
        bad = {"title": "Time Machine 2", "publication_year": future, "author": self.author1.id}
        bad_response = self.client.post(url, bad, format="json")
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", bad_response.data)

    # ---------- Update
    def test_update_book_requires_auth(self):
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        resp = self.client.patch(url, {"title": "Beloved (Edited)"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_success(self):
        self._auth()
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        resp = self.client.patch(url, {"title": "Beloved (Edited)"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Beloved (Edited)")

    # ---------- Delete
    def test_delete_book_requires_auth(self):
        url = reverse("book-delete", kwargs={"pk": self.book2.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_success(self):
        self._auth()
        url = reverse("book-delete", kwargs={"pk": self.book2.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # ---------- Filtering (django-filter)
    def test_filter_by_exact_year(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"publication_year": 1992})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertEqual(titles, ["Jazz"])

    def test_filter_by_year_range(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"year_min": 1970, "year_max": 1995})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = sorted([b["title"] for b in resp.json()])
        self.assertEqual(titles, ["Beloved", "Jazz"])

    def test_filter_by_author_id(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"author": self.author2.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Things Fall Apart")

    def test_filter_by_author_name_icontains(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"author_name": "toni"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = sorted([b["title"] for b in resp.json()])
        self.assertEqual(titles, ["Beloved", "Jazz"])

    def test_filter_by_title_icontains(self):
        url = reverse("book-list")
        resp = self.client.get(url, {"title": "fall"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()[0]["title"], "Things Fall Apart")

    # ---------- Search (?search= over title and author__name)
    def test_search_over_title_and_author(self):
        url = reverse("book-list")

        # Search by title fragment
        resp = self.client.get(url, {"search": "belov"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertIn("Beloved", titles)

        # Search by author name fragment
        resp = self.client.get(url, {"search": "achebe"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertEqual(titles, ["Things Fall Apart"])

    # ---------- Ordering
    def test_ordering_by_publication_year(self):
        url = reverse("book-list")

        # Ascending
        resp = self.client.get(url, {"ordering": "publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles_asc = [b["title"] for b in resp.json()]
        self.assertEqual(titles_asc, ["Things Fall Apart", "Beloved", "Jazz"])

        # Descending
        resp = self.client.get(url, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles_desc = [b["title"] for b in resp.json()]
        self.assertEqual(titles_desc, ["Jazz", "Beloved", "Things Fall Apart"])
        
    def setUp(self):
        self.client = APIClient()     
