import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            type=str,
            help='foodgram/data/ingredients.csv',
        )

    def handle(self, *args, **options):
        path = options['csv_path']
        created_count = 0
        skipped_count = 0

        with open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                name, unit = row[0], row[1]
                _, created = Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=unit,
                )
                if created:
                    created_count += 1
                else:
                    skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Создано: {created_count}, пропущено: {skipped_count}'
            )
        )
