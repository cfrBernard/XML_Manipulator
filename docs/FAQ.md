# FAQ

### Table of Contents

- [1. Can I use absolute or relative paths for the input file?](#1-can-i-use-absolute-or-relative-paths-for-the-input-file)
- [2. Where are the output files stored?](#2-where-are-the-output-files-stored)
- [3. What happens when I use `--dry-run`?](#3-what-happens-when-i-use---dry-run)
- [4. How does merging handle duplicate items?](#4-how-does-merging-handle-duplicate-items)
- [5. How does the `--bycolor` option determine color names?](#5-how-does-the---bycolor-option-determine-color-names)
- [6. Does the tool preserve the order of items?](#6-does-the-tool-preserve-the-order-of-items)
- [7. What if the XML contains malformed or incomplete entries?](#7-what-if-the-xml-contains-malformed-or-incomplete-entries)
- [8. Do I need to run `python app.py init` before using the tool?](#8-do-i-need-to-run-python-apppy-init-before-using-the-tool)
- [9. Does the tool modify my original XML file?](#9-does-the-tool-modify-my-original-xml-file)

---

### 1. Can I use absolute or relative paths for the input file?

Yes. Both are supported. 

**Examples**:

```
--input parts.xml                # If the file is in assets/input/
```
```
--input assets/input/parts.xml   # Explicit path
```

---

### 2. Where are the output files stored?

Output files are created in a folder inside `assets/output/` using a timestamped name.

This ensures that multiple runs never overwrite previous results.

---

### 3. What happens when I use `--dry-run`?

No files or folders are created.

The tool only prints what would happen, allowing you to preview the split or merge process safely.

---

### 4. How does merging handle duplicate items?

If two items share the same `ITEMID` and `COLOR`, they are merged into a single entry.

Their `QTY` values are summed automatically.

---

### 5. How does the `--bycolor` option determine color names?

Color names come directly from the `<COLOR>` tags in the source XML.

The tool does not translate, rename, or map colors to BrickLink or Rebrickable conventions.

---

### 6. Does the tool preserve the order of items?

Yes. Items appear in the same order as in the original XML, except when duplicates are merged (those collapse into a single entry).

---

### 7. What if the XML contains malformed or incomplete entries?

If expected tags are missing (e.g., missing `QTY`), the tool applies safe default values to avoid crashes.

---

### 8. Do I need to run `python app.py init` before using the tool?

No. This command simply pre-creates the folder structure, but it’s optional – the tool automatically creates missing folders when needed.

---

### 9. Does the tool modify my original XML file?

No. The source XML is never edited in place.

The tool only reads it, processes it, and writes new files in the output directory.

---