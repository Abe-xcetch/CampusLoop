from django.core.management.base import BaseCommand
from listings.models import Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seed the marketplace category table with default categories."

    def handle(self, *args, **options):
        categories = [
            "Books",
            "Electronics",
            "Fashion",
            "Furniture",
            "Sports",
            "Services",
            "Others",
        ]

        created_count = 0
        for name in categories:
            slug = slugify(name)
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": f"{name} category for campus marketplace listings.",
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {name}"))

        self.stdout.write(self.style.SUCCESS(f"Seed complete. {created_count} categories created."))
