from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.template.loader import get_template
from weasyprint import HTML


@dataclass
class PdfRenderer:
    """Render HTML templates into PDF bytes using WeasyPrint."""

    @staticmethod
    def render(context: dict[str, Any], template_name: str) -> bytes:
        template = get_template(template_name)
        html = template.render(context)
        return HTML(string=html).write_pdf()
