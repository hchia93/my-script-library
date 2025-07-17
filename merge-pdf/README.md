# Merge PDF

This is a Python script to merge images (PNG, JPG) and PDF files into a single output PDF.

## Use case
Best for people who has lot scanned document and needed to bundle scanned image into one pdf file. This is a good utility script that can replace the scanner software that combines scanned documents.

## Prerequisites

- Install Python 3.6+
- Install dependencies by running this file on terminal.

```bat
install.bat
```

## Example 

| Mode       | Description    | Example Usage  |
|------------|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `-merge`   | Manually specify individual files and optional PDF page ranges. Can optionally specify page number or a range of pages, separated by `,`                                  | `python merge-pdf.py -merge "/path/doc1.pdf [1, 3:5]" "/path/image1.png" -o "/path/output.pdf"` |
| `-blob`    | Merge all `.pdf`, `.png`, `.jpg`, `.jpeg` files from a directory, sorted alphabetically by name. | `python merge-pdf.py -blob "/path/to/folder" -o "/path/output.pdf"`                             |

