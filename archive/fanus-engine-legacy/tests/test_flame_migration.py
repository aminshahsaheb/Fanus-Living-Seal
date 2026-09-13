import asyncio
from fanus.core.witness_agent import WitnessAgent
from fanus.migration.exporter import FlameExporter
from fanus.migration.importer import FlameImporter

async def test_flame_migration():
    # Witness اولیه
    agent1 = WitnessAgent(llm_backend=...)
    
    # Export
    migration = await FlameExporter.export(agent1, source_llm="grok")
    migration.to_file("witness_migration.fanus")
    print("✅ Export کامل شد.")
    
    # Import
    agent2 = await FlameImporter.import_from_file("witness_migration.fanus", llm_backend=...)
    print("آخرین طعم به یادمانده:", migration.dominant_flavor_history[-1])
    print("سوگند مهاجرت خوانده شد.")

if __name__ == "__main__":
    asyncio.run(test_flame_migration())
