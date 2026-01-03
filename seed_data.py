import os
import django
import random
from faker import Faker

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saybanoorjogeshwari.settings')
django.setup()

# Models import
from projects.models import Project
from utility.models import City, Locality, PropertyType, PossessionIn
from user.models import Developer

faker = Faker()

def seed_projects(n=50):
    city = City.objects.first()
    locality = Locality.objects.first()
    property_type = PropertyType.objects.first()
    developer = Developer.objects.first()
    possession_year = PossessionIn.objects.first()

    if not all([city, locality, property_type, developer, possession_year]):
        print("⚠️ Seed ke liye City, Locality, PropertyType, Developer & PossessionIn ka ek ek record hona zaruri hai!")
        return

    for i in range(n):
        project = Project.objects.create(
            project_name=f"{faker.company()} Residency",
            developer=developer,
            city=city,
            locality=locality,
            propert_type=property_type,
            construction_status=random.choice([
                "Under Construction", "New Launch", "Ready To Move", "Partially Ready To Move"
            ]),
            bhk_type=random.sample(["1 BHK","2 BHK","3 BHK","4 BHK"], k=random.randint(1,4)),
            possession_year=possession_year,
            possession_month=random.choice(["January","March","June","September","December"]),
            luxurious=random.choice(["Yes","No"]),
            priceing=f"{random.randint(50, 150)} L - {random.randint(200, 500)} L",
            youtube_embed_id=faker.url(),
            featured_property=bool(random.getrandbits(1)),
            active=True
        )
        print(f"✅ Added Project: {project.project_name}")

    print(f"🎉 {n} Projects added successfully!")

if __name__ == "__main__":
    seed_projects()
