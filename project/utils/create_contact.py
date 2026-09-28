import os
import sys
from pathlib import Path
from random import choice

import django
from django.conf import settings


# Caminho base do projeto
DJANGO_BASE_DIR = Path(__file__).resolve().parent.parent

# Quantidade de contatos criados
NUMBER_OF_OBJECTS = 1000


# Adiciona o projeto no caminho do Python
sys.path.append(str(DJANGO_BASE_DIR))

# Configura o Django
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'project.settings'
)

settings.USE_TZ = False

django.setup()


if __name__ == '__main__':
    import faker

    from contact.models import Category, Contact

    # Apaga dados antigos
    Contact.objects.all().delete()
    Category.objects.all().delete()

    fake = faker.Faker('pt_BR')

    categories = [
        'Amigos',
        'Família',
        'Conhecidos'
    ]

    # Criando categorias
    django_categories = [
        Category(name=name)
        for name in categories
    ]

    Category.objects.bulk_create(django_categories)

    # Atualiza categorias com os IDs criados
    django_categories = list(Category.objects.all())

    django_contacts = []

    # Criando contatos falsos
    for _ in range(NUMBER_OF_OBJECTS):

        profile = fake.profile()

        email = profile['mail']

        first_name, last_name = str(
            profile['name']
        ).split(' ', 1)

        phone = fake.phone_number()

        create_date = fake.date_this_year()

        description = fake.text(
            max_nb_chars=100
        )

        category = choice(
            django_categories
        )

        django_contacts.append(
            Contact(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                create_date=create_date,
                description=description,
                category=category,
            )
        )

    # Salva todos os contatos de uma vez
    if django_contacts:
        Contact.objects.bulk_create(
            django_contacts
        )

    print(
        f'{NUMBER_OF_OBJECTS} contatos criados com sucesso!'
    )