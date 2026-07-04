import time


class KnowledgeGraph:

    def __init__(self):
        self.entities = {}
        self.relations = []
        self.evidence = []

    def add_entity(self, name, entity_type, confidence=1.0):
        if name not in self.entities:
            self.entities[name] = {
                "name": name,
                "type": entity_type,
                "confidence": confidence,
                "created": time.time()
            }
        return self.entities[name]

    def add_relation(self, from_entity, relation, to_entity, confidence=1.0):
        r = {
            "from": from_entity,
            "relation": relation,
            "to": to_entity,
            "confidence": confidence,
            "timestamp": time.time()
        }
        self.relations.append(r)
        return r

    def add_evidence(self, claim, source, confidence=1.0):
        e = {
            "claim": claim,
            "source": source,
            "confidence": confidence,
            "timestamp": time.time()
        }
        self.evidence.append(e)
        return e

    def snapshot(self):
        return {
            "entities": len(self.entities),
            "relations": len(self.relations),
            "evidence": len(self.evidence)
        }