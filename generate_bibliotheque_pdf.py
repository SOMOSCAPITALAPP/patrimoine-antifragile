from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "bibliotheque-antifragile-source.txt"
OUTPUT = ROOT / "bibliotheque-antifragile.pdf"


def build_pdf() -> None:
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleBlue",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=HexColor("#0b4fd6"),
        spaceAfter=12,
    )
    body = ParagraphStyle(
        "BodyBlue",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        textColor=HexColor("#1b2a3a"),
        spaceAfter=8,
    )
    section = ParagraphStyle(
        "SectionBlue",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=HexColor("#081321"),
        spaceBefore=8,
        spaceAfter=8,
    )

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []

    first_title = True
    for raw_line in lines:
      line = raw_line.strip()
      if not line:
          story.append(Spacer(1, 5))
          continue
      if first_title:
          story.append(Paragraph(line, title))
          first_title = False
          continue
      if line[0].isdigit() and ". " in line:
          story.append(Paragraph(line, section))
      else:
          story.append(Paragraph(line.replace("&", "&amp;"), body))

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title="Bibliotheque Antifragile",
        author="Patrimoine Antifragile",
    )
    doc.build(story)


if __name__ == "__main__":
    build_pdf()
