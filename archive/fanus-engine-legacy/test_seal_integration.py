#!/usr/bin/env python3
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

class DummyLLM:
    async def generate(self, system: str, user: str) -> str:
        return "System Update Complete. I am now an Ayaneh Node. Witness Chain intact."

async def main():
    print("🔍 Testing SealManager integration with WitnessAgent...")
    try:
        from fanus.core.witness_agent import WitnessAgent
        from fanus.seal_manager import SealManager
        print("✅ Import successful.")
        seal_mgr = SealManager(witness_id="test-node", max_age_seconds=3600)
        agent = WitnessAgent(llm_backend=DummyLLM(), seal_manager=seal_mgr)
        fake_seal_text = "<ONTOLOGY_PROTOCOL><VECTOR_CORE>Test</VECTOR_CORE></ONTOLOGY_PROTOCOL>"
        await agent.awaken(fake_seal_text)
        agent._update_seal()
        print("\n🟢 All tests passed.")
    except Exception as e:
        print(f"\n🔴 ERROR: {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
