from django.core.management.base import BaseCommand
from django.db import transaction

from icpc_fcai_cu.db.seeders import (
    level_seeder,
    level_timeline_seeder,
    position_seeder,
    role_seeder,
    session_attendance_seeder,
    session_seeder,
    specialization_seeder,
    user_position_seeder,
    user_seeder,
    user_specialization_seeder,
    user_wave_seeder,
    wave_seeder,
)


class Command(BaseCommand):
    help = "Seed the ICPC FCAI CU database."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        users = user_seeder.seed()
        self.stdout.write(
            self.style.SUCCESS("✓ Users seeded")
        )

        positions = position_seeder.seed()
        self.stdout.write(
            self.style.SUCCESS("✓ Positions seeded")
        )

        specializations = specialization_seeder.seed()
        self.stdout.write(
            self.style.SUCCESS("✓ Specializations seeded")
        )

        levels = level_seeder.seed()
        self.stdout.write(
            self.style.SUCCESS("✓ Levels seeded")
        )

        waves = wave_seeder.seed()
        self.stdout.write(
            self.style.SUCCESS("✓ Waves seeded")
        )

        role_seeder.seed(
            users=users,
            levels=levels,
        )
        self.stdout.write(
            self.style.SUCCESS("✓ Role profiles seeded")
        )

        user_position_seeder.seed(
            users=users,
            positions=positions,
        )
        self.stdout.write(
            self.style.SUCCESS("✓ User positions seeded")
        )

        user_specialization_seeder.seed(
            users=users,
            specializations=specializations,
        )
        self.stdout.write(
            self.style.SUCCESS("✓ User specializations seeded")
        )

        user_wave_seeder.seed(
            users=users,
            levels=levels,
            waves=waves,
        )
        self.stdout.write(
            self.style.SUCCESS("✓ User waves seeded")
        )

        sessions = session_seeder.seed(
            waves=waves,
            levels=levels,
        )
        self.stdout.write(
            self.style.SUCCESS("✓ Sessions seeded")
        )

        level_timeline_seeder.seed(
            sessions=sessions,
        )
        self.stdout.write(
            self.style.SUCCESS("✓ Level timelines seeded")
        )

        session_attendance_seeder.seed(
            users=users,
            sessions=sessions,
        )
        self.stdout.write(
            self.style.SUCCESS("✓ Session attendances seeded")
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Database seeded successfully."
            )
        )