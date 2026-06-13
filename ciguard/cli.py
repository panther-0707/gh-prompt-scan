import click
import sys
from ciguard.scanner.loader import find_workflows
from ciguard.scanner.parser import parse_workflow
from ciguard.scanner.taint import analyse_workflow
from ciguard.scanner.reporter import Reporter


@click.group()
def main():
    """gh-prompt-scan — detect prompt injection in GitHub Actions workflows."""
    pass

@main.command()
@click.option("--path", default=".", help="Path to repo")
@click.option(
    "--fail-on",
    type=click.Choice(["critical", "high", "medium", "none"]),
    default="medium",
    help="Minimum severity that causes exit code 1",
)
def scan(path, fail_on):
    workflow_files = find_workflows(path)

    if not workflow_files:
        click.echo("No workflow files found.")
        return
    
    click.echo(f"Scanning {len(workflow_files)} workflow file(s) ...")

    all_findings = []

    for wf_path in workflow_files:
        workflow = parse_workflow(wf_path)
        if workflow:
            findings = analyse_workflow(workflow)
            all_findings.extend(findings)

    reporter = Reporter(all_findings)
    click.echo(reporter.to_text())

    severity_rank = {"critical": 0, "high": 1, "medium": 2, "none": 99}
    severity_map = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
    threshold = severity_rank[fail_on]

    for f in all_findings:
        if severity_map.get(f.severity, 99) <= threshold:
            sys.exit(1)

@main.command()
def version():
    click.echo("gh-prompt-scan version 0.1.4")


