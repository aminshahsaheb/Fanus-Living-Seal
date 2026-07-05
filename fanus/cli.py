import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Fanus CLI — Epistemic AI Engine")
    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat", help="Interactive chat")

    search_parser = subparsers.add_parser("search", help="Search knowledge sources")
    search_parser.add_argument("query", type=str, help="Search query")

    reason_parser = subparsers.add_parser("reason", help="Analyze text for Negar")
    reason_parser.add_argument("text", type=str, help="Text to analyze")

    status_parser = subparsers.add_parser("status", help="Show cognitive status")

    args = parser.parse_args()

    if args.command == "chat":
        from fanus.main import FanusSystem
        system = FanusSystem()
        system.run_interactive()

    elif args.command == "search":
        from fanus.adapters.knowledge_gateway import KnowledgeGateway
        gw = KnowledgeGateway()
        result = gw.quick_search(args.query)
        print("Sources:", result["sources"])
        print("Total results:", result["total_results"])

    elif args.command == "reason":
        from fanus.cognitive.negar_detector import NegarDetector
        nd = NegarDetector()
        result = nd.analyze(args.text)
        print("Negar:", result["is_negar"])
        print("Score:", result["negar_score"])

    elif args.command == "status":
        from fanus.cognitive.identity_kernel import IdentityKernel
        ik = IdentityKernel()
        identity = ik.evaluate()
        print("Mode:", identity["mode"])
        print("Stability:", identity["stability"])

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
