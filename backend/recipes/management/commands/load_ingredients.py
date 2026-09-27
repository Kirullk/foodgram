import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            type=str,
            help='Путь к CSV-файлу с ингредиентами',
        )

    def handle(self, *args, **options):
        path = options['csv_path']
        ingredients = []

        with open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                name, unit = row
                ingredients.append(
                    Ingredient(name=name, measurement_unit=unit)
                )

        Ingredient.objects.bulk_create(
            ingredients,
            ignore_conflicts=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Загружено ингредиентов: {len(ingredients)}'
            )
        )
