from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from src.catalog.models import NationalCuisine, Recipe, Category

User = get_user_model()


class HomepageViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("homepage"))

    def test_call_view_load(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "catalog/homepage.html")


class RecipeListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        for i in range(11):
            category = Category.objects.create(title=f"Category Title {i}")
            national_cuisine = NationalCuisine.objects.create(title=f"National Cuisine Title {i}")
            Recipe.objects.create(
                title=f"Recipe Title {i}",
                author=user,
                duration=timezone.timedelta(0, 600),
                category=category,
                national_cuisine=national_cuisine,
                is_draft=False
            )

    def setUp(self):
        self.response = self.client.get(reverse("recipe_list"))

    def test_call_view_load(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "catalog/recipe_list.html")

    def test_pagination_is_ten(self):
        response = self.response
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipes"]), 10)

    def test_pagination_next_page(self):
        response = self.client.get(reverse("recipe_list") + "?page=2")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipes"]), 1)


class UserRecipeListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        for i in range(13):
            category = Category.objects.create(title=f"Category Title {i}")
            national_cuisine = NationalCuisine.objects.create(title=f"National Cuisine Title {i}")
            is_draft = False
            if i == 11:
                user = User.objects.create_user(email="test_views_0@test.ru", password="password")
            if i == 12:
                is_draft = True
            Recipe.objects.create(
                title=f"Recipe Title {i}",
                author=user,
                duration=timezone.timedelta(0, 600),
                category=category,
                national_cuisine=national_cuisine,
                is_draft=is_draft
            )

    def setUp(self):
        self.client.login(email="test_views_0@test.ru", password="password")
        author = User.objects.get(email="test_views@test.ru")
        self.response = self.client.get(reverse("user_recipe_list", kwargs={'author_id': author.id}))

    def test_call_view_load(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "catalog/user_recipe_list.html")

    def test_pagination_is_ten(self):
        response = self.response
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipes"]), 10)

    def test_pagination_next_page(self):
        author = User.objects.get(email="test_views@test.ru")
        response = self.client.get(reverse("user_recipe_list", kwargs={'author_id': author.id}) + "?page=2")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["recipes"]), 1)

    def test_contains_drafts_if_request_user_is_the_author(self):
        user = User.objects.get(email="test_views_0@test.ru")
        response = self.client.get(reverse("user_recipe_list", kwargs={'author_id': user.id}))
        self.assertEqual(len(response.context["recipes"]), 2)

    def test_does_not_contains_drafts_if_request_user_is_not_the_author(self):
        self.client.logout()
        self.client.login(email="test_views@test.ru", password="password")
        author = User.objects.get(email="test_views_0@test.ru")
        response = self.client.get(reverse("user_recipe_list", kwargs={'author_id': author.id}))
        self.assertEqual(len(response.context["recipes"]), 1)


class RecipeDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        for i in range(2):
            category = Category.objects.create(title=f"Category Title {i}")
            national_cuisine = NationalCuisine.objects.create(title=f"National Cuisine Title {i}")
            is_draft = False
            if i == 1:
                is_draft = True
            Recipe.objects.create(
                title=f"Recipe Title {i}",
                author=user,
                duration=timezone.timedelta(0, 600),
                category=category,
                national_cuisine=national_cuisine,
                is_draft=is_draft
            )

    def setUp(self):
        self.response = self.client.get(reverse(
            "recipe_detail",
            kwargs={'pk': Recipe.objects.get(title="Recipe Title 0", is_draft=False).id}
        ))

    def test_call_view_load(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "catalog/recipe_detail.html")
    
    def test_not_found_if_is_draft(self):
        response = self.client.get(reverse(
            "recipe_detail",
            kwargs={'pk': Recipe.objects.get(title="Recipe Title 1", is_draft=True).id}
        ))
        self.assertEqual(response.status_code, 404)


class RecipeCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="test_views@test.ru", password="password")

    def test_redirect_if_request_user_is_not_logged_in(self):
        response = self.client.get(reverse("recipe_create"))
        self.assertRedirects(response, reverse("account_login") + "?next=" + reverse("recipe_create"))

    def test_access_permitted_if_request_user_is_logged_in(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_create"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_create"))
        self.assertTemplateUsed(response, "catalog/recipe_form.html")

    def test_view_context_contains_optional_forms(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_create"))
        self.assertTrue("ingredient_formset" in response.context)
        self.assertTrue("direction_formset" in response.context)


class RecipeUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        User.objects.create_user(email="test_views_0@test.ru", password="password")
        category = Category.objects.create(title="Category Title")
        national_cuisine = NationalCuisine.objects.create(title="National Cuisine Title")
        Recipe.objects.create(
            title="Recipe Title",
            author=user,
            duration=timezone.timedelta(0, 600),
            category=category,
            national_cuisine=national_cuisine,
            is_draft=True
        )

    def test_redirect_if_request_user_is_not_logged_in(self):
        response = self.client.get(reverse("recipe_update", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertRedirects(response, reverse("account_login") + "?next=" + reverse(
            "recipe_update",
            kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}
        ))

    def test_access_denied_if_request_user_is_not_the_author(self):
        self.client.login(email="test_views_0@test.ru", password="password")
        response = self.client.get(reverse("recipe_update", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertEqual(response.status_code, 403)

    def test_access_permitted_if_request_user_is_the_author(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_update", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertEqual(response.status_code, 200)

    def test_view_context_contains_optional_forms(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_update", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertTrue("ingredient_formset" in response.context)
        self.assertTrue("direction_formset" in response.context)

    def test_view_uses_correct_template(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_update", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertTemplateUsed(response, "catalog/recipe_form.html")


class RecipeDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test_views@test.ru", password="password")
        User.objects.create_user(email="test_views_0@test.ru", password="password")
        category = Category.objects.create(title="Category Title")
        national_cuisine = NationalCuisine.objects.create(title="National Cuisine Title")
        Recipe.objects.create(
            title="Recipe Title",
            author=user,
            duration=timezone.timedelta(0, 600),
            category=category,
            national_cuisine=national_cuisine,
            is_draft=True
        )

    def test_redirect_if_request_user_is_not_logged_in(self):
        response = self.client.get(reverse("recipe_delete", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertRedirects(response, reverse("account_login") + "?next=" + reverse(
            "recipe_delete",
            kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}
        ))
    
    def test_access_denied_if_request_user_is_not_the_author(self):
        self.client.login(email="test_views_0@test.ru", password="password")
        response = self.client.get(reverse("recipe_delete", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertEqual(response.status_code, 403)

    def test_access_permitted_if_request_user_is_the_author(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_delete", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.get(reverse("recipe_delete", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertTemplateUsed(response, "catalog/recipe_confirm_delete.html")
    
    def test_success_url(self):
        self.client.login(email="test_views@test.ru", password="password")
        response = self.client.post(reverse("recipe_delete", kwargs={'pk': Recipe.objects.get(title="Recipe Title").id}))
        self.assertRedirects(response, reverse("homepage"))
