"""Check that the built CV reads cleanly as text, the way an ATS parser sees it.

Extracts the text with pypdf, pdfminer and poppler's pdftotext (when installed)
and fails if any of them sees something a recruiter's software could trip on.

    pip install pypdf pdfminer.six
    python scripts/ats_check.py cv.pdf
"""
import re
import shutil
import subprocess
import sys

import pypdf
from pdfminer.high_level import extract_text

PAGES = 2
HEADINGS = ["EDUCATION", "EXPERIENCE", "PROJECTS", "SKILLS"]
EMAIL = "contact@michadasis.com"
PHONE = "+30 697 585 2293"
MUST_CONTAIN = ["Ioannis Michadasis", "github.com/michadasis", "in/johnmichadasis", "Πληροφορική"]
# letters (any script), digits and whitespace are always fine, plus these
ALLOWED = set(".,;:()/&'+-–·@#%!?\"")

pdf = sys.argv[1] if len(sys.argv) > 1 else "cv.pdf"
failures = []


def fail(msg):
    failures.append(msg)
    print(f"  FAIL {msg}")


reader = pypdf.PdfReader(pdf)

print("PDF")
if len(reader.pages) != PAGES:
    fail(f"{len(reader.pages)} pages, expected {PAGES}")
for i, page in enumerate(reader.pages, 1):
    for font in (page["/Resources"].get("/Font") or {}).values():
        font = font.get_object()
        name = font.get("/BaseFont")
        desc = font.get("/FontDescriptor")
        if "/DescendantFonts" in font:
            desc = font["/DescendantFonts"][0].get_object().get("/FontDescriptor")
        desc = desc.get_object() if desc else {}
        if not any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")):
            fail(f"page {i}: font {name} is not embedded")
        if "/ToUnicode" not in font:
            fail(f"page {i}: font {name} has no ToUnicode map, its text can't be read back")
print(f"  {len(reader.pages)} pages, fonts checked")

texts = {
    "pypdf": "\n".join(p.extract_text() for p in reader.pages),
    "pdfminer": extract_text(pdf),
}
if shutil.which("pdftotext"):
    texts["pdftotext"] = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", pdf, "-"], capture_output=True, check=True
    ).stdout.decode("utf-8")
else:
    print("  (pdftotext not installed, skipping poppler)")

for name, text in texts.items():
    print(name)
    before = len(failures)
    for h in HEADINGS:
        if not re.search(rf"\b{h}\b", text):
            fail(f"{name}: heading {h} not found as one word")
    spaced = re.findall(r"\b(?:[A-Z] ){3,}[A-Z]\b", text)
    if spaced:
        fail(f"{name}: letters read as separate words: {spaced}")
    split_numbers = re.findall(r"\d [.,](?:\d|\s)", text)
    if split_numbers:
        fail(f"{name}: number split by a space before punctuation: {split_numbers}")
    odd = sorted({c for c in text if not (c.isalnum() or c.isspace() or c in ALLOWED)})
    if odd:
        fail(f"{name}: unexpected characters {odd}")
    if EMAIL not in text:
        fail(f"{name}: email {EMAIL} not found")
    if PHONE not in text:
        fail(f"{name}: phone {PHONE} not found")
    for s in MUST_CONTAIN:
        if s not in text:
            fail(f"{name}: {s!r} not found")
    if len(failures) == before:
        print("  ok")

if failures:
    print(f"\n{len(failures)} problem(s)")
    sys.exit(1)
print("\nAll checks passed")
