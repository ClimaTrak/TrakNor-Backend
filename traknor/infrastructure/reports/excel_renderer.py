from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Any

import pandas as pd


@dataclass
class ExcelRenderer:
    """Render datasets into Excel using pandas."""

    @staticmethod
    def render(context: dict[str, Any], sheet_name: str) -> bytes:
        df = pd.DataFrame(context.get("rows", []))
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        return output.getvalue()
