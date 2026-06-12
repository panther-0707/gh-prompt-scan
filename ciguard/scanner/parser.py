import yaml
from pathlib import Path
from dataclasses import dataclass, field


# A single step inside a job
# e.g. "- run: pytest" or "- uses: actions/checkout@v4"
@dataclass
class WorkflowStep:
    name: str
    uses: str | None        # which action this step calls (if any)
    run: str | None         # shell command (if any)
    env: dict               # environment variables
    with_inputs: dict       # inputs passed to an action
    if_condition: str | None  # optional condition like "if: github.actor == 'bot'"


# A job is a group of steps
# e.g. the "build" job or the "test" job
@dataclass
class WorkflowJob:
    name: str
    steps: list[WorkflowStep]
    if_condition: str | None
    permissions: dict


# The whole workflow file
@dataclass
class Workflow:
    path: Path
    name: str
    triggers: dict       # the "on:" block — what fires this workflow
    permissions: dict    # what the workflow is allowed to do
    jobs: dict[str, WorkflowJob]


def parse_workflow(path: Path) -> Workflow | None:
    """
    Read a workflow YAML file and return a Workflow object.
    Returns None if the file can't be parsed.
    """
    try:
        # Open the file and parse the YAML into a Python dictionary
        with open(path) as f:
            raw = yaml.safe_load(f)

        # If the file is empty or not a dictionary, skip it
        if not isinstance(raw, dict):
            return None

        # Parse each job and its steps
        jobs = {}
        for job_name, job_data in (raw.get("jobs") or {}).items():
            
            steps = []
            for step in (job_data.get("steps") or []):
                steps.append(WorkflowStep(
                    name=step.get("name", ""),
                    uses=step.get("uses"),
                    run=step.get("run"),
                    env=step.get("env") or {},
                    with_inputs=step.get("with") or {},
                    if_condition=step.get("if"),
                ))

            jobs[job_name] = WorkflowJob(
                name=job_name,
                steps=steps,
                if_condition=job_data.get("if"),
                permissions=job_data.get("permissions") or {},
            )

        return Workflow(
            path=path,
            name=raw.get("name", str(path)),
            triggers=raw.get(True) or raw.get("on") or {},
            permissions=raw.get("permissions") or {},
            jobs=jobs,
        )

    except Exception:
        # If anything goes wrong just skip this file
        return None