import glob
from pathlib import Path


def find_workflows(base_path = ".") -> list[Path]:
    # Find all the Github actions workflow YAML files in the repository.

    patterns = [
        base_path + "/.github/workflows/*.yml",
        base_path + "/.github/workflows/*.yaml",
    ]

    files = []

    for pattern in patterns:  
        results = glob.glob(pattern)
        
        for file in results:
            files.append(Path(file))

    return files