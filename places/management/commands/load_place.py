import requests

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

    def _validate(self, place_data):
        for field in ('title', 'description_short', 'description_long', 'coordinates'):
            if field not in place_data:
                raise CommandError(f'В JSON отсутствует обязательное поле: "{field}"')
        coords = place_data['coordinates']
        if 'lng' not in coords or 'lat' not in coords:
            raise CommandError('В JSON.coordinates отсутствуют "lng" или "lat"')

    def handle(self, *args, **options):
        url = options['url']

        place_data = self._load_json(url)
        self._validate(place_data)

        title = (place_data['title'] or '').strip()
        if not title:
            raise CommandError('Поле "title" пустое.')

        if Place.objects.filter(title=title).exists():
            raise CommandError(f'Место с таким title уже существует: "{title}"')

        try:
            lng = float(place_data['coordinates']['lng'])
            lat = float(place_data['coordinates']['lat'])
        except (TypeError, ValueError):
            raise CommandError('Некорректные координаты: ожидаются числа (lng/lat).')

        description_short = (place_data.get('description_short') or '').strip()
        description_long = (place_data.get('description_long') or '').strip()
        imgs = place_data.get('imgs') or []

        with transaction.atomic():
            place = Place.objects.create(
                title=title,
                description_short=description_short,
                description_long=description_long,
                lng=lng,
                lat=lat,
            )

            base_name = slugify(title, allow_unicode=True)
            for idx, img_url in enumerate(imgs):
                content = self._download_bytes(img_url)
                filename = f'{base_name}_{idx}.jpg'
                pic = PlaceImage(place=place, order=idx)
                pic.image.save(filename, ContentFile(content), save=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Добавлено место: {title} (id={place.pk}), загруженно изображений: {len(imgs)}'
            )
        )
