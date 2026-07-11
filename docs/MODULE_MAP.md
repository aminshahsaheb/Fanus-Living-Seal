# Fanus Module Map

## fanus/core/
| File | Purpose | Status |
|------|---------|--------|
| identity.py | FanusIdentity — system prompt from seal | ✅ |
| seal.py | FanusSeal — SHA3-512 + XML parsing | ✅ |
| seal_verifier.py | Identity integrity check | ✅ |
| novayin.py | NOVAYIN_LEXICON — 11 core terms | ✅ |
| plugin_system.py | Dynamic adapter registration | ✅ |
| architecture_map.py | Architecture reference | ✅ |
| seed.py | Core seed values | ✅ |
| version_core.py | Version management | ✅ |

## fanus/cognitive/
| File | Purpose | Status |
|------|---------|--------|
| identity_kernel.py | Stability-based identity | ✅ |
| self_model.py | Drift + coherence tracking | ✅ |
| collapse/ | Collapse risk monitoring | ✅ |
| evolution/ | Evolution proposals | ✅ |
| hayrat_judge.py | Post-LLM epistemic evaluation | ✅ |
| fi_detector.py | Identity/Emotional/Epistemic flattery | ✅ |
| negar_detector.py | Flattery + overconfidence | ✅ |
| policy_engine.py | Signal → Fanus event routing | ✅ |
| isp_controller.py | Identity safeguard protocol | ✅ |
| judgment_layer.py | Semantic event enrichment | ✅ |
| goal_engine.py | Persistent goal tracking | ✅ |
| curiosity_engine.py | Question generation | ✅ |
| orchestrator.py | Cognitive growth coordinator | ✅ |

## fanus/memory/
| File | Purpose | Status |
|------|---------|--------|
| ledger.py | Event ledger | ✅ |
| knowledge_graph.py | Entity/Relation/Evidence | ✅ |
| evidence_engine.py | Claim validation | ✅ |
| scientific_validator.py | Evidence scoring | ✅ |
| belief_layer.py | FACT/THEORY/HYPOTHESIS/OPINION | ✅ |
| conflict_resolver.py | Competing claims | ✅ |
| source_ranking.py | Source confidence hierarchy | ✅ |
| knowledge_compression.py | Multi-claim synthesis | ✅ |
| memory_replay.py | Decay-based consolidation | ✅ |
| pipeline.py | Unified memory orchestrator | ✅ |
| persistence.py | State persistence | ✅ |

## fanus/runtime/
| File | Purpose | Status |
|------|---------|--------|
| loop.py | FanusLoop — main cognitive loop | ✅ |
| observer/ | Runtime trace recording | ✅ |
| safety/ | Hard guards + safety gates | ✅ |
| self_stabilization_engine.py | Adaptive stability control | ✅ |
| decision/ | Decision engine | ✅ |

## fanus/adapters/
| File | Purpose | Status |
|------|---------|--------|
| groq_adapter.py | Groq LLM | ✅ Active |
| claude_adapter.py | Anthropic Claude | ✅ Ready |
| openai_adapter.py | OpenAI | ✅ Ready |
| arxiv_adapter.py | ArXiv papers | ✅ Active |
| crossref_adapter.py | Crossref DOI | ✅ Active |
| pubmed_adapter.py | PubMed | ✅ Active |
| wikipedia_adapter.py | Wikipedia | ✅ Active |
| github_adapter.py | GitHub repos | ✅ Active |
| hackernews_adapter.py | Hacker News | ✅ Active |
| knowledge_gateway.py | Unified 6-source search | ✅ Active |

## fanus/api/
| File | Purpose | Status |
|------|---------|--------|
| server.py | FastAPI main server | ✅ Live |
| demo.py | Public demo endpoints | ✅ Live |
| knowledge.py | Knowledge endpoints | ✅ Live |
| reasoning.py | Negar + contradiction | ✅ Live |
| research.py | Research planning | ✅ Live |
| memory.py | Memory endpoints | ✅ Live |
| decision.py | Goals + governance | ✅ Live |
| automation.py | Auto research loop | ✅ Live |
| auth.py | API key authentication | ✅ Live |

## fanus/audit/  ← در حال ساخت
| File | Purpose | Status |
|------|---------|--------|
| audit_engine.py | Verify orchestrator | 🔨 |
