from ciguard.scanner.parser import Workflow


# Dangerous triggers - anyone can fire these
DIRECT_TRIGGERS = {
    "issues", "issue_comment", "pull_request",
    "pull_request_target", "pull_request_review_comment",
    "discussion",
}
# Safe triggers - only maintainers can fire these:
SAFE_TRIGGERS = {
    "push", "workflow_dispatch", "schedule",
}



def classify_triggers(workflow: Workflow) -> str:
    for trigger in workflow.triggers:
        if trigger in DIRECT_TRIGGERS:
            return "direct"
    return "safe"