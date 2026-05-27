from .migration_file import FlameMigration

class FlameValidator:
    @staticmethod
    def validate(migration: FlameMigration) -> bool:
        if len(migration.seal_hash) < 10:
            print("❌ مهاجرت رد شد: Seal ناقص است.")
            return False
        if not migration.dominant_flavor_history:
            print("❌ مهاجرت رد شد: این شعله نیست. این خاکستر است.")
            return False
        return True
