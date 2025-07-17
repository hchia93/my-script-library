import re
from pathlib import Path
from typing import List, Union
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter


def parse_page_spec(spec: str) -> List[int]:
    if not spec.startswith('[') or not spec.endswith(']'):
        raise ValueError("Invalid page specification format.")
    inner = spec[1:-1]
    pages = []
    for part in inner.split(','):
        part = part.strip()
        if ':' in part:
            start, end = map(int, part.split(':'))
            pages.extend(range(start - 1, end))
        else:
            pages.append(int(part) - 1)
    return pages


def add_pdf(writer: PdfWriter, filepath: Path, pages: Union[List[int], None]):
    reader = PdfReader(str(filepath))
    total = len(reader.pages)
    if pages is None:
        pages = list(range(total))
    for page_num in pages:
        if 0 <= page_num < total:
            writer.add_page(reader.pages[page_num])
        else:
            print(f"⚠️ Skipping invalid page {page_num+1} in {filepath.name}")


def add_image(writer: PdfWriter, filepath: Path):
    image = Image.open(filepath).convert("RGB")
    tmp_path = filepath.with_suffix(".temp.pdf")
    image.save(tmp_path, "PDF", resolution=100.0)
    reader = PdfReader(str(tmp_path))
    writer.add_page(reader.pages[0])
    tmp_path.unlink(missing_ok=True)


def handle_merge_mode(inputs: List[str], output_path: str):
    writer = PdfWriter()
    for item in inputs:
        match = re.match(r'^(.+\.(pdf|PDF))\s*(\[.*\])?$', item)
        pages = None

        if match:
            filepath = Path(match.group(1)).expanduser().resolve()
            if match.group(3):
                try:
                    pages = parse_page_spec(match.group(3))
                except Exception as e:
                    print(f"❌ Page spec error in {item}: {e}")
                    continue
        else:
            filepath = Path(item).expanduser().resolve()

        if not filepath.exists():
            print(f"❌ File not found: {filepath}")
            continue

        if filepath.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            add_image(writer, filepath)
        elif filepath.suffix.lower() == '.pdf':
            add_pdf(writer, filepath, pages)
        else:
            print(f"❌ Unsupported file type: {filepath}")

    with open(output_path, 'wb') as f:
        writer.write(f)
    print(f"✅ Merged PDF written to: {output_path}")


def handle_blob_mode(blob_dir: str, output_path: str):
    writer = PdfWriter()
    dir_path = Path(blob_dir).expanduser().resolve()
    if not dir_path.is_dir():
        print(f"❌ Directory not found: {blob_dir}")
        return

    files = sorted(dir_path.glob("*"))
    for file in files:
        if file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            add_image(writer, file)
        elif file.suffix.lower() == '.pdf':
            add_pdf(writer, file, None)

    with open(output_path, 'wb') as f:
        writer.write(f)
    print(f"✅ Blob PDF created from folder: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Merge selective PDF pages and images into a single PDF.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-merge', nargs='+', help='Input files with optional page spec, e.g. "/abs/path/file.pdf [1,3:5]"')
    group.add_argument('-blob', help='Merge all PDF/image files in a folder (alphabetical order)')
    parser.add_argument('-o', '--output', required=True, help='Output PDF path')
    args = parser.parse_args()

    if args.merge:
        handle_merge_mode(args.merge, args.output)
    elif args.blob:
        handle_blob_mode(args.blob, args.output)


if __name__ == "__main__":
    main()
