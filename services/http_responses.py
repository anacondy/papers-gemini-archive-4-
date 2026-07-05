"""HTML response builders used by route handlers."""

HTML_ERROR_TEMPLATE = """
<style>
    body {{ font-family: sans-serif; background-color: #1a1a1a; color: #e0e0e0; padding: 40px; }}
    h1 {{ color: #4CAF50; }}
    p {{ color: #bbb; }}
    a {{ display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #4CAF50;
         color: white; text-decoration: none; border-radius: 4px; }}
    a:hover {{ background-color: #45a049; }}
</style>
<h1>{title}</h1>
<p>{message}</p>
{links}
"""

HTML_SUCCESS_TEMPLATE = """
<style>
    body {{ font-family: sans-serif; background-color: #1a1a1a; color: #e0e0e0; padding: 40px; }}
    h1 {{ color: #4CAF50; }}
    p {{ color: #bbb; }}
    a {{ display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #4CAF50;
         color: white; text-decoration: none; border-radius: 4px; }}
    a:hover {{ background-color: #45a049; }}
</style>
<h1>File Uploaded Successfully!</h1>
<p>Metadata has been written directly into the PDF properties.</p>
<p><strong>Saved as:</strong> {filename}</p>
<a href="/">Go to Home Page</a>
<a href="/admin">Upload Another</a>
"""


def create_html_response(template, **kwargs):
    """Render one of the inline HTML templates with keyword arguments."""
    return template.format(**kwargs)


def create_error_response(title, message, links=""):
    """Build a standard styled error response body."""
    return create_html_response(HTML_ERROR_TEMPLATE, title=title, message=message, links=links)


def create_success_response(filename):
    """Build a standard styled success response body."""
    return create_html_response(HTML_SUCCESS_TEMPLATE, filename=filename)
