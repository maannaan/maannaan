"""
Single source of truth for everything personal in this profile README.

Generators import from here, so changing bio/stack/handle is a one-file edit.

Regenerate after editing:
  python scripts/prep_badge.py
  python scripts/make_control_room.py
  python scripts/make_mission_dossiers.py
  python scripts/fetch_contributions.py
  python scripts/render_heatmap_svg.py
  python scripts/fetch_ops_log.py
"""

# ---- identity -------------------------------------------------------------
GITHUB_USER = "maannaan"
FULL_NAME = "Manan Paliwal"
TAGLINE = "DevOps & Cloud Platform Engineer · Kadel Labs"
ROLE_LINE = "Platform Engineer @ Kadel Labs"
LOCATION = "Udaipur, Rajasthan"
CERT_CHIP = "RHCSA 2025"

PROMPT_USER = "manan"
PROMPT_HOST = "ops"

# First year with contributions (heatmap scrape walks year-by-year from here).
ACCOUNT_START_YEAR = 2023

# ---- control room ---------------------------------------------------------
CLOUDS = [
    {"name": "AWS", "status": "healthy", "detail": "EKS · S3 · IAM"},
    {"name": "Azure", "status": "healthy", "detail": "AKS · DevOps"},
    {"name": "GCP", "status": "healthy", "detail": "GKE · Cloud Run"},
    {"name": "Proxmox", "status": "healthy", "detail": "On-prem · DR"},
]

PIPELINE_STAGES = [
    "commit",
    "build",
    "scan",
    "deploy",
    "observe",
]

FOCUS_TILES = [
    {
        "title": "Kubernetes Platform",
        "body": "Multi-tenant SaaS · Helm · GitOps",
    },
    {
        "title": "AI Infrastructure",
        "body": "WhisperX · Ollama · vLLM · MCP",
    },
    {
        "title": "Observability",
        "body": "Prometheus · Grafana · OTel · Datadog",
    },
]

# ---- mission dossiers -----------------------------------------------------
MISSIONS = [
    {
        "id": "D-001",
        "title": "Enterprise Kubernetes Platform",
        "outcome": "Multi-tenant SaaS platform across AWS, Azure, and GCP",
        "stack": "Helm · GitOps · Kafka · Prometheus",
    },
    {
        "id": "D-002",
        "title": "WhisperX AI Infrastructure",
        "outcome": "GPU transcription services with batch ETL at scale",
        "stack": "Docker · GPU · ETL · Linux",
    },
    {
        "id": "D-003",
        "title": "AI Agent & Local LLM Platform",
        "outcome": "Self-hosted multi-agent orchestration without external deps",
        "stack": "LangGraph · CrewAI · Ollama · Vault",
    },
]
