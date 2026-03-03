import json
from pathlib import Path

from lead_scoring.io import load_leads, resolve_data_path
from lead_scoring.pipeline import run_pipeline


def _write_leads_file(path: Path) -> None:
    payload = [
        {
            "id": "lead_001",
            "email": "sarah.connor@sky-net.org",
            "raw_note": "We are a cybersecurity firm with about 250 employees.",
        }
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_load_leads_parses_records(tmp_path):
    leads_file = tmp_path / "leads.json"
    _write_leads_file(leads_file)

    leads = load_leads(leads_file)
    assert len(leads) == 1
    assert leads[0].id == "lead_001"


def test_resolve_data_path_prefers_explicit_path(tmp_path):
    leads_file = tmp_path / "custom_leads.json"
    _write_leads_file(leads_file)

    resolved = resolve_data_path(leads_file)
    assert resolved == leads_file


def test_run_pipeline_with_explicit_data_path(tmp_path):
    leads_file = tmp_path / "custom_leads.json"
    _write_leads_file(leads_file)

    result = run_pipeline(data_path=leads_file)

    assert len(result) == 1
    assert result[0]["id"] == "lead_001"
    assert "score" in result[0]
    assert "crm_action" in result[0]
