# XML_Manipulator

![Version](https://img.shields.io/badge/version-v1.1.0-blue)
[![License](https://img.shields.io/github/license/cfrBernard/XML_Manipulator)](./LICENSE.md)

This tool was created to help LEGO enthusiasts manage their BrickLink collections efficiently. Often, Rebrickable's free plan limits the number of unique parts per list, and manually splitting large XML inventories can be tedious. XML Manipulator automates this process, allowing you to:

- Analyze your XML inventory (number of total pieces and unique parts)
- Split large inventories into multiple files, each respecting the maximum unique parts limit
- Optionally perform dry runs to preview the splits

> No dependencies are required beyond Python 3, making it fast, portable, and easy to use.

---

## Installation

1. Clone this repository:
```
git clone https://github.com/cfrBernard/XML_Manipulator.git
```

```
cd XML_Manipulator
```
2. Ensure you have Python 3 installed.
3. Place your BrickLink XML file in `assets/input/`.

> No further installation is needed. No .venv needed too.

---

## Usage

The tool is a single CLI script: `app.py`. It provides two main commands: `stats` and `split`.

### General Help

```
python app.py -h
```

```
usage: app.py [-h] {stats,split} ...


XML Manipulator for BrickLink inventories


positional arguments:
{stats,split} sub-command help
stats Show stats about an XML inventory
split Split an XML into chunks of unique parts


optional arguments:
-h, --help show this help message and exit
```

## 1. Stats

Show basic statistics about your BrickLink inventory.

### Command:

```
python app.py stats --input assets/input/parts.xml
```

### Output example:

```
Total physical pieces: 42817
Unique items: 1342
```

## 2. Split 

Split your inventory XML into multiple files, each containing up to a specified number of unique parts.

### Command:

```
python app.py split --input assets/input/parts.xml --max 1000 --verbose
```

### Options:

- `--max` → maximum unique parts per file (default: 1000)
- `--verbose` → show detailed processing messages
- `--dry-run` → simulate the split without writing files

### Dry-run example:

```
python app.py split --input assets/input/parts.xml --max 1000 --dry-run --verbose
```

### Output example:

```
[INFO] Total unique items: 1342
[INFO] Will generate 2 files.
[DRY] Would write: assets/output/2025-11-11_22-10-00/output_1.xml
[DRY] Would write: assets/output/2025-11-11_22-10-00/output_2.xml
```

> - **File output**: Files are written to `assets/output/<timestamp>/output_1.xml`, `output_2.xml`, etc.

---

## 🔮 What's Coming:

- Quiet mode / reduced verbosity: run without printing [INFO] messages by default
- Chunk preview command: display how many output files would be created and unique items per chunk before writing
- Export CSV: generate a CSV with part IDs, colors, and quantities
- Merge multiple XML files: combine several inventories into one
- Filter options: split or analyze by color, part type, or custom filters
- Log coloring: make [INFO], [OK], [DRY] visually distinct for better readability
- Desktop interface

---

## Notes: 

- For more information about the version, please refer to the [changelog](docs/CHANGELOG.md) section.

- This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

- You can write the input path in absolute or relative form:
    ```
    --input parts.xml (If it is in assets/input/)
    
    OR
    
    --input assets/input/parts.xml
    ```

---

## 🤝 Contact:
For issues, suggestions, or contributions, feel free to open an issue on the GitHub repository.

---

> Created for LEGO enthusiasts who want fast, dependency-free manipulation of BrickLink XML inventories.
