"""
Single source of truth for everything personal in this profile README.

Every generator (portrait, info card, heatmap) imports from here, so changing
your bio/stack/handle is a one-file edit -- no hunting through SVG builders.

Regenerate after editing:
  python scripts/fetch_contributions.py
  python scripts/render_heatmap_svg.py
  python scripts/make_info_card.py
  python scripts/prep_photo.py source-photo.jpg && python scripts/make_ascii_svg.py
"""

# ---- identity -------------------------------------------------------------
GITHUB_USER = "maannaan"
FULL_NAME = "Manan Paliwal"
TAGLINE = "DevOps & Cloud Platform Engineer · Kadel Labs"

# shell prompt shown in each terminal-style SVG titlebar ("<PROMPT_USER>@ops")
PROMPT_USER = "manan"
PROMPT_HOST = "ops"

# First year with contributions. GitHub's public endpoint only serves a rolling
# 12-month window, so fetch_contributions.py walks year-by-year from here.
ACCOUNT_START_YEAR = 2023

# ---- info card rows -------------------------------------------------------
# ("host",) -> "<PROMPT_USER>@ops" + rule
# ("kv", key, value) -> amber key + light value
# ("sec", title) -> steel-blue section header
# ("bul", text) -> teal bullet
# ("gap",) -> vertical space
ROWS = [
    ("host",),
    ("kv", "Now", "DevOps Engineer @ Kadel Labs"),
    ("kv", "Focus", "AWS · GCP · Proxmox · AI Infra"),
    ("kv", "Before", "Webanix · Easewin · Codenscious"),
    ("kv", "Edu", "B.Tech CSE — RTU Kota (9.3 CGPA)"),
    ("kv", "Cert", "RHCSA 2025"),
    ("kv", "Based", "Udaipur, Rajasthan"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Cloud", "AWS, Azure, GCP"),
    ("kv", "Containers", "Kubernetes, Docker, Helm, EKS/AKS"),
    ("kv", "IaC / CI", "Terraform, Ansible, Jenkins, Actions"),
    ("kv", "Observability", "Prometheus, Grafana, OTel, Datadog"),
    ("kv", "AI Infra", "LangGraph, CrewAI, Ollama, vLLM"),
    ("gap",),
    ("sec", "Highlights"),
    ("bul", "Enterprise multi-cloud Kubernetes platform"),
    ("bul", "WhisperX GPU transcription infrastructure"),
    ("bul", "Local LLM & multi-agent platform (MCP)"),
]
