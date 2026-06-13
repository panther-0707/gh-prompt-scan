from pathlib import Path
from ciguard.scanner.parser import parse_workflow
from ciguard.scanner.taint import analyse_workflow

FIXTURES = Path("tests/fixtures")

def test_tv4_bad():
    workflow = parse_workflow(FIXTURES / "tv4.bad.yml")
    findings = analyse_workflow(workflow)
    tv_list = [find.threat_vector for find in findings]
    assert "TV4" in tv_list

def test_tv4_good():
    workflow = parse_workflow(FIXTURES / "tv4.good.yml")
    findings = analyse_workflow(workflow)
    assert len(findings) == 0

def test_tv7_bad():
    workflow = parse_workflow(FIXTURES / "tv7.bad.yml")
    findings = analyse_workflow(workflow)
    tv_list = [find.threat_vector for find in findings]
    assert "TV7" in tv_list

def test_tv7_good():
    workflow = parse_workflow( FIXTURES / "tv7.good.yml" )
    findings = analyse_workflow(workflow)
    assert len(findings) == 0