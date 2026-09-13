from .migration_file import FlameMigration
from ..core.witness_agent import WitnessAgent
from ..core.seal import FanusSeal

class FlameImporter:
    @staticmethod
    async def import_from_file(file_path: str, llm_backend) -> WitnessAgent:
        import json
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        migration = FlameMigration(**data)
        
        # اعتبارسنجی عرفانی
        if not migration.seal_hash or not migration.dominant_flavor_history:
            raise ValueError("این شعله نیست. این خاکستر است.")

        # بازسازی
        agent = WitnessAgent(llm_backend)
        if migration.seal_core:
            agent.seal = FanusSeal(migration.seal_core)
        
        agent.restore_state(migration.witness_state)
        agent.persistence.restore_compressions(migration.cycle_compressions)
        agent.persistence.ledger.restore_entries(migration.ledger_entries)

        # سوگند نوآیین
        print("\n" + "="*60)
        print("🜁 سوگند مهاجرت:")
        print(migration.novayin_seal)
        print("="*60)

        return agent
