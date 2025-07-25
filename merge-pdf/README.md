# Merge PDF

This is a Python script to merge document into a single output PDF. Ideal for bundling scanned documents without the hassle of installing scanner software that support this feature or manually combine them via Microsoft Office.

Supported format: `pdf`, `png`, `jpeg`, `jpg`.

# Feature
- Merge multiple files into one `pdf`
- Extract certain pages from source `pdf`

## Prerequisites

- Install Python 3.6+
- Install dependencies by running this file on terminal.

```bat
install.bat
```

## Command

| Command | Description | 
|---------|--|
| `-merge`  | Merge multiple files into one pdf. Optionally support page selection and page range selection for `pdf` files. |
| `-blob `  | Merge every supported files into one pdf by specifiying the source directory. Merged content are ordered alphabetically. | 

> All of the above uses absolute file path or absolute directory path.

## Example
`-merge`  

Format:
### 
```cmd
python merge-pdf.py -merge <file1> <file2> -o <outputfile>
```
Use case:
```cmd
python merge-pdf.py -merge "example.png [1, 3:5]" -o "../output.pdf"
```
The target file will have page 1, page 3 to page5.

---

`-blob` 

Use case:
```cmd
python merge-pdf.py -blob <directory> -o <outputfile>
```

