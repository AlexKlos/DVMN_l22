import requests
import sys
import time

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from places.models import Place, PlaceImage

TIMEOUT = 20


class Command(BaseCommand):
    help = 'Загружает данные для нового места из JSON по URL и сохраняет в БД.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL файла .json с описанием места')

    def _load_json(self, url):
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _download_bytes(self, url):
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.content

    def _validate(self, place_info):
        for field in ('title', 'short_description', 'long_description', 'coordinates'):
            if field not in place_info:
                raise CommandError(f'В JSON отсутствует обязательное поле: "{field}"')
        coords = place_info['coordinates']
        if 'lng' not in coords or 'lat' not in coords:
            raise CommandError('В JSON.coordinates отсутствуют "lng" или "lat"')

    def handle(self, *args, **options):
        url = options['url']

        place_info = self._load_json(url)
        self._validate(place_info)

        title = (place_info['title'] or '').strip()
        if not title:
            raise CommandError('Поле "title" пустое.')

        place, created = Place.objects.get_or_create(
            title=title,
            defaults={
                'short_description': short_description,
                'long_description': long_description,
                'lng': lng,
                'lat': lat,
            }
        )
        if not created:
            raise CommandError(f'Место с таким title уже существует: "{title}"')

        try:
            lng = float(place_info['coordinates']['lng'])
            lat = float(place_info['coordinates']['lat'])
        except (TypeError, ValueError):
            raise CommandError('Некорректные координаты: ожидаются числа (lng/lat).')

        short_description = (place_info.get('short_description') or '').strip()
        long_description = (place_info.get('long_description') or '').strip()
        imgs = place_info.get('imgs') or []

        with transaction.atomic():
            place = Place.objects.create(
                title=title,
                short_description=short_description,
                long_description=long_description,
                lng=lng,
                lat=lat,
            )

            base_name = slugify(title, allow_unicode=True)
            for idx, img_url in enumerate(imgs):
                try:
                    content = self._download_bytes(img_url)
                except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
                    print(f'Ошибка при загрузке {img_url}: {e}', file=sys.stderr)
                    if isinstance(e, requests.exceptions.ConnectionError):
                        time.sleep(5)
                    continue
                
                filename = f'{base_name}_{idx}.jpg'
                PlaceImage.objects.create(place=place, order=idx, image=ContentFile(content, name=filename))

        self.stdout.write(
            self.style.SUCCESS(
                f'Добавлено место: {title} (id={place.pk}), загруженно изображений: {len(imgs)}'
            )
        )
