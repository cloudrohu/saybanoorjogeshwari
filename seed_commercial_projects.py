from django.core.management.base import BaseCommand
from faker import Faker
import random
from projects.models import Project
from utility.models import City, Locality, PropertyType
from user.models import Developer

fake = Faker()

class Command(BaseCommand):
    help = "Seed fake Commercial Projects using Faker"

    def handle(self, *args, **kwargs):
        # Make sure some City, Locality, Developer, PropertyType exists
        cities = list(City.objects.all())
        localities = list(Locality.objects.all())
        developers = list(Developer.objects.all())
        property_types = PropertyType.objects.filter(title__icontains='commercial') | PropertyType.objects.filter(title__icontains='office')

        if not cities or not localities or not developers or not property_types:
            self.stdout.write(self.style.ERROR("⚠️ Make sure City, Locality, Developer, and Commercial PropertyType exist."))
            return

        for _ in range(10):  # 10 fake projects
            city = random.choice(cities)
            locality = random.choice(localities)
            developer = random.choice(developers)
            prop_type = random.choice(property_types)

            project_name = fake.company() + " Tower"
            month = random.choice(['January','February','March','April','May','June','July','August','September','October','November','December'])
            year = random.choice([2024, 2025, 2026, 2027])

            project = Project.objects.create(
                project_name=project_name,
                developer=developer,
                city=city,
                locality=locality,
                propert_type=prop_type,
                construction_status=random.choice(['New Launch','Under Construction','Ready To Move']),
                possession_month=month,
                possession_year_id=1,  # ⚠️ Change if you have a real PossessionIn object
                luxurious=fake.word(),
                priceing=str(random.randint(5000000, 80000000)),  # ₹50L to ₹8Cr
                active=True,
                featured_property=random.choice([True, False]),
                youtube_embed_id=random.choice(['ptl5G1rcnUY','gkQj_9R9HG8','dQw4w9WgXcQ'])
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Added Commercial Project: {project.project_name}"))

        self.stdout.write(self.style.SUCCESS("🎉 Fake Commercial Projects Seeded Successfully!"))
