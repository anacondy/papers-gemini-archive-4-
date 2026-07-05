"""Paper indexing helpers for `/api/papers` responses."""

import os
import re


PAPER_FILENAME_PATTERN = re.compile(
    r"\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_(.*\.pdf)",
    re.IGNORECASE,
)


def list_papers(upload_folder, url_builder):
    """Parse tagged filenames from upload folder and emit API-ready dicts."""
    papers = []

    if not os.path.exists(upload_folder):
        return papers

    for filename in os.listdir(upload_folder):
        match = PAPER_FILENAME_PATTERN.match(filename)
        if not match:
            continue

        groups = match.groups()
        papers.append(
            {
                "class": groups[0],
                "subject": groups[1],
                "semester": groups[2].replace("Sem-", ""),
                "year": groups[3],
                "exam_type": groups[4],
                "medium": groups[5],
                "uploader": groups[6],
                "original_name": groups[7],
                "url": url_builder(filename),
            }
        )

    return papers
