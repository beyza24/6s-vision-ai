"""docs/PROJE-RAPORU.md dosyasından yazdırılabilir PDF üretir."""
from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "PROJE-RAPORU.md"
OUT = ROOT / "docs" / "PROJE-RAPORU.pdf"
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
NAVY = (14, 31, 58)
BLUE = (37, 99, 235)
INK = (28, 36, 51)
MUTED = (90, 102, 122)


class Report(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("Arial", "", 9)
        self.set_text_color(*MUTED)
        self.set_xy(18, 10)
        self.cell(0, 6, "6S-VISION AI  ·  Proje raporu", align="L")
        self.set_draw_color(*BLUE)
        self.set_line_width(0.4)
        self.line(18, 17, 192, 17)
        self.ln(12)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("Arial", "", 9)
        self.set_text_color(*MUTED)
        self.cell(0, 8, f"{self.page_no()}", align="C")


def usable(pdf: FPDF) -> float:
    return pdf.w - pdf.l_margin - pdf.r_margin


def write_rich(pdf: FPDF, text: str, size: float, height: float) -> None:
    pdf.set_text_color(*INK)
    parts = re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text)
    for part in parts:
        if not part:
            continue
        bold = (part.startswith("**") and part.endswith("**")) or (
            part.startswith("`") and part.endswith("`")
        )
        if bold:
            part = part[2:-2] if part.startswith("**") else part[1:-1]
        pdf.set_font("Arial", "B" if bold else "", size)
        width = pdf.get_string_width(part)
        room = pdf.w - pdf.r_margin - pdf.get_x()
        if bold and width > room and width < usable(pdf):
            pdf.ln(height)
            pdf.set_x(pdf.l_margin)
        pdf.write(height, part)


def paragraph(pdf: FPDF, text: str) -> None:
    pdf.set_x(pdf.l_margin)
    write_rich(pdf, text, 11, 6)
    pdf.ln(8)


def bullet(pdf: FPDF, text: str, marker: str = "•") -> None:
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(*BLUE)
    pdf.write(6, f"{marker}  ")
    write_rich(pdf, text, 11, 6)
    pdf.ln(7)


def heading(pdf: FPDF, text: str, level: int) -> None:
    if level == 1:
        return
    pdf.ln(2)
    pdf.set_x(pdf.l_margin)
    if level == 2:
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(*NAVY)
        pdf.multi_cell(usable(pdf), 8, text)
        pdf.set_draw_color(*BLUE)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.l_margin + 28, y)
        pdf.ln(4)
        return
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(usable(pdf), 7, text)
    pdf.ln(1)


def code_block(pdf: FPDF, lines: list[str]) -> None:
    pdf.set_fill_color(244, 247, 252)
    pdf.set_font("Arial", "", 9.5)
    pdf.set_text_color(*NAVY)
    text = "\n".join(lines)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(usable(pdf), 5, text, fill=True)
    pdf.ln(4)


def table(pdf: FPDF, rows: list[list[str]]) -> None:
    if not rows:
        return
    width = usable(pdf)
    cols = len(rows[0])
    col_w = width / cols
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(255, 255, 255)
    pdf.set_draw_color(220, 226, 236)
    for cell in rows[0]:
        pdf.cell(col_w, 8, cell, border=0, fill=True)
    pdf.ln(8)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(*INK)
    for index, row in enumerate(rows[1:]):
        if index % 2:
            pdf.set_fill_color(255, 255, 255)
        else:
            pdf.set_fill_color(244, 247, 252)
        heights = []
        for cell in row:
            heights.append(pdf.multi_cell(col_w, 5, cell, dry_run=True, output="LINES"))
        line_count = max(len(item) for item in heights)
        row_h = max(8, line_count * 5 + 2)
        if pdf.get_y() + row_h > pdf.h - 20:
            pdf.add_page()
        y0 = pdf.get_y()
        x0 = pdf.l_margin
        for cell in row:
            pdf.set_xy(x0, y0)
            pdf.rect(x0, y0, col_w, row_h, style="F")
            pdf.multi_cell(col_w, 5, cell)
            x0 += col_w
        pdf.set_y(y0 + row_h)
    pdf.ln(4)


def cover(pdf: FPDF) -> None:
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 46, style="F")
    pdf.set_fill_color(*BLUE)
    pdf.rect(0, 46, 210, 2.2, style="F")
    pdf.set_xy(18, 12)
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "6S-VISION AI", align="L")
    pdf.set_xy(18, 26)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Proje raporu", align="L")
    pdf.set_y(58)
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(usable(pdf), 6, "ICAAD 2026  ·  AI-Deathon  ·  Selçuk Üniversitesi\n24 Ekim 2026")
    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(usable(pdf), 7, "Yapay zekâ görür, insan karar verir.")
    pdf.ln(3)


def build() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    pdf = Report(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("Arial", "", str(FONT))
    pdf.add_font("Arial", "B", str(FONT_BOLD))
    pdf.set_margins(18, 22, 18)
    pdf.add_page()
    cover(pdf)

    in_code = False
    skip_diagram = False
    code: list[str] = []
    table_rows: list[list[str]] = []
    in_table = False

    def flush_table() -> None:
        nonlocal table_rows, in_table
        if table_rows:
            table(pdf, table_rows)
        table_rows = []
        in_table = False

    started = False
    for raw in lines:
        line = raw.rstrip()
        if not started:
            if line.startswith("## "):
                started = True
            else:
                continue
        if line.startswith("```"):
            if in_code:
                if not skip_diagram:
                    code_block(pdf, code)
                code = []
                in_code = False
                skip_diagram = False
            else:
                flush_table()
                in_code = True
                skip_diagram = line.strip() == "```mermaid"
            continue
        if in_code:
            if not skip_diagram:
                code.append(line)
            continue
        if line.startswith("|"):
            cells = [re.sub(r"[`*]", "", cell.strip()) for cell in line.strip("|").split("|")]
            if all(set(cell) <= {"-", ":"} or not cell for cell in cells):
                continue
            in_table = True
            table_rows.append(cells)
            continue
        if in_table:
            flush_table()
        if not line.strip():
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            heading(pdf, line[3:].strip(), 2)
            continue
        if line.startswith("### "):
            heading(pdf, line[4:].strip(), 3)
            continue
        if line.startswith("- "):
            bullet(pdf, line[2:].strip())
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)", line)
        if numbered:
            bullet(pdf, numbered.group(2), marker=f"{numbered.group(1)}.")
            continue
        paragraph(pdf, line)

    flush_table()
    pdf.output(str(OUT))
    print(f"yazildi {OUT} ({OUT.stat().st_size} bayt)")


if __name__ == "__main__":
    build()
