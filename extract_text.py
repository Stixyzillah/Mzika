import fitz  # PyMuPDF
import re
import json

# Step 1: Open PDF
pdf_path = "Malawi Constitution.pdf"  # Update if path differs
doc = fitz.open(pdf_path)

# Step 2: Extract and clean all pages
full_text = ""
for page in doc:
    full_text += page.get_text()
doc.close()

# Normalize spacing
full_text = re.sub(r'\n+', '\n', full_text)
full_text = re.sub(r'\s{2,}', ' ', full_text)

# Step 3: Split by chapters
chapter_splits = re.split(r'(CHAPTER\s+[IVXLCDM]+)', full_text, flags=re.IGNORECASE)

chapters = []
i = 1
while i < len(chapter_splits) - 1:
    chapter_number = chapter_splits[i].strip()
    chapter_text = chapter_splits[i + 1].strip()

    # Step 4: Split into sections using "digit." format (e.g., 15. Right to Life)
    section_pattern = re.compile(r'(\d+\.\s+[^0-9]+)')
    parts = section_pattern.split(chapter_text)

    sections = []
    if parts:
        for j in range(1, len(parts), 2):
            number = parts[j].strip()
            content = parts[j + 1].strip() if j + 1 < len(parts) else ""
            sections.append({
                "section": number,
                "content": content
            })

    chapters.append({
        "chapter": chapter_number,
        "sections": sections
    })
    i += 2

# Step 5: Save as JSON
with open("constitution.json", "w", encoding="utf-8") as f:
    json.dump(chapters, f, indent=2, ensure_ascii=False)

print("✅ Extracted and saved to constitution.json")
