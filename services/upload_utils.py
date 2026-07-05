"""Upload validation and PDF metadata helper utilities."""

import os
from pypdf import PdfReader, PdfWriter
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):
    """Return True if filename has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def sanitize(text):
    """Allow only safe filename/form characters used by this app."""
    if not text:
        return ""
    return "".join(c for c in text if c.isalnum() or c in (" ", "_", "-")).rstrip()


def extract_sanitized_fields(form):
    """Normalize and sanitize all upload form fields into one dict."""
    return {
        "admin_name": sanitize(form.get("admin_name", "")),
        "class_name": sanitize(form.get("class", "")),
        "subject": sanitize(form.get("subject", "")),
        "semester": sanitize(form.get("semester", "")),
        "exam_year": sanitize(form.get("exam_year", "")),
        "exam_type": sanitize(form.get("exam_type", "")),
        "medium": sanitize(form.get("medium", "")),
        "time": sanitize(form.get("time", "N/A")),
        "max_marks": sanitize(form.get("max_marks", "N/A")),
    }


def build_storage_filename(fields, original_filename):
    """Build the tagged storage filename used by the search/index parser."""
    tags = [
        fields["class_name"],
        fields["subject"],
        f"Sem-{fields['semester']}",
        fields["exam_year"],
        fields["exam_type"],
        fields["medium"],
        fields["admin_name"],
    ]
    filename_prefix = "_".join(f"[{tag}]" for tag in tags)
    original_secure_name = secure_filename(original_filename)
    original_base, original_ext = os.path.splitext(original_secure_name)
    return os.path.basename(f"{filename_prefix}_{original_base}{original_ext}")


def file_size_exceeds_limit(file_storage, max_file_size):
    """Check file size without consuming the upload stream permanently."""
    file_storage.seek(0, os.SEEK_END)
    file_size = file_storage.tell()
    file_storage.seek(0)
    return file_size > max_file_size


def write_pdf_metadata(filepath, fields):
    """Write searchable metadata into the uploaded PDF and persist in place."""
    reader = PdfReader(filepath)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    keywords = (
        f"{fields['class_name']}, {fields['exam_year']}, Sem {fields['semester']}, "
        f"{fields['exam_type']}, {fields['medium']}, Time: {fields['time']}, Marks: {fields['max_marks']}"
    )

    writer.add_metadata(
        {
            "/Author": fields["admin_name"],
            "/Title": f"{fields['class_name']} - {fields['subject']} (Sem {fields['semester']})",
            "/Subject": fields["subject"],
            "/Keywords": keywords,
        }
    )

    with open(filepath, "wb") as out_file:
        writer.write(out_file)


def validate_safe_serving_path(upload_folder, requested_filename):
    """Validate and normalize a requested upload filename for secure serving.

    Returns the sanitized filename when safe, else returns None.
    """
    filename = os.path.basename(requested_filename)

    if os.path.sep in filename or (os.path.altsep and os.path.altsep in filename):
        return None

    filepath = os.path.join(upload_folder, filename)
    upload_folder_abs = os.path.abspath(upload_folder)
    filepath_abs = os.path.abspath(filepath)

    if not filepath_abs.startswith(upload_folder_abs + os.path.sep) and filepath_abs != upload_folder_abs:
        return None

    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return None

    return filename
