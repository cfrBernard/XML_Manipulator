# XML_Manipulator

![Version](https://img.shields.io/badge/version-v1.6.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

This tool was created to help LEGO enthusiasts manage their BrickLink collections efficiently. Often, Rebrickable's free plan limits the number of unique parts per list, and manually splitting large XML inventories can be tedious. XML Manipulator automates this process, allowing you to:

- Analyze your XML inventory (number of total pieces, unique parts, unique colors)
- Split large inventories into multiple files, each respecting the maximum unique parts limit
- **Optionally split per color** using `--bycolor`
- Merge multiple XML files from a folder into a single inventory file
- Optionally perform dry runs to preview the splits

> No dependencies are required beyond Python 3, making it fast, portable, and easy to use.

---

## Installation

1. Clone this repository:

```
git clone https://github.com/cfrBernard/XML_Manipulator.git
cd XML_Manipulator
```

2. Ensure you have Python 3 installed.
3. Initialize the folder structure:

```
python app.py init
```

4. Place your BrickLink XML file in `assets/input/`.

> No further installation is needed. No .venv needed too.

---

## Usage

The tool is a single CLI script: `app.py`. It provides three main commands: `stats`, `split` and `merge`.

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
merge Merge all XML files in a folder into one


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
[INFO] Total physical pieces: 42817
[INFO] Unique items: 1342
[INFO] Different colors: 36
```

## 2. Split 

Split your inventory XML into multiple files, based on unique parts or by grouping items per color.

### Classic split command:

```
python app.py split --input assets/input/parts.xml --max 1000 --verbose
```

### By-color split command:

```
python app.py split --input assets/input/parts.xml --bycolor --max 1000 --verbose
```

### Options:

- `--max` → maximum number of unique items per generated file (default: 1000)
- `--bycolor` → split the inventory **separately for each color**  
    - Each color is processed independently  
    - Output files will be named `output_<COLOR>_<index>.xml`
- `--verbose` → show detailed processing messages
- `--dry-run` → simulate the split without writing files
    - Works for `classic` and `--bycolor` modes

### Dry-run example:

```
python app.py split --input assets/input/parts.xml --max 1000 --dry-run --verbose
```

### Output example:

```
[INFO] Total unique items: 1342
[INFO] Will generate 2 files.
[DRY] Would write: assets/output/<timestamp>/output_1.xml
[DRY] Would write: assets/output/<timestamp>/output_2.xml
```

> **Output location:**  
> Generated files are stored in `assets/output/<timestamp>/`.

## 3. Merge

Merge multiple XML files into a single inventory file. By default, it merges all XML files in `assets/input/merge/`.

### Command:

```
python app.py merge --input-dir assets/input/merge --output assets/output/merged.xml --verbose
```

### Options

- `--input-dir` → folder containing XML files to merge (**default**: `assets/input/merge/`)
- `--output` → path for the merged XML (**default**: `assets/output/merged_{timestamp}.xml`)
- `--verbose` → show detailed processing messages
- `--dry-run` → simulate the merge without writing the file

### Dry-run example:

```
python app.py merge --dry-run --verbose
```

### Output example:

```
[INFO] Found 3 XML files in assets/input/merge
[DRY] Would write merged file to: assets/output/merged_<timestamp>.xml
```

> **Merge behavior**: Duplicate items (same `ITEMID` and `COLOR`) are automatically combined by summing quantities.

---

## 🔮 What's Coming:

- Export CSV: generate a CSV with part IDs, colors, and quantities
- Filter options: split or analyze by part type, or custom filters
- Proper documentation (sry for that o_o)
- Desktop interface

---

## Notes:

- You can write the input path in absolute or relative form:
    ```
    --input parts.xml (If it is in assets/input/)
    
    OR
    
    --input assets/input/parts.xml
    ```

- The output folder is automatically created using a timestamp, so running multiple splits never overwrites previous results.

- When using `--dry-run`, no folders or files are created – only a preview of the actions is displayed.

- Merging automatically combines duplicate items (same ITEMID + COLOR). Quantities are summed so the output contains only unique entries.

- When using `--bycolor`, color names come directly from the XML (`<COLOR>` tags). The tool does **not** translate or rename colors.

- The tool keeps the order of ITEM elements as they appear in the XML, except when items are merged (duplicates collapse into one).

- If an XML file contains unexpected structures or missing tags (e.g., missing QTY), default values are applied safely.

- Running `python app.py init` is optional – the tool will create missing folders automatically whenever needed.

- The application only reads and writes XML files; it never modifies the original source file.

- For more information about the version, please refer to the [changelog](docs/CHANGELOG.md) section.

- This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---

## ⚠️ Warning / Disclaimer

- This tool is provided **as-is**. While it has been tested on multiple inventories, **bugs may still exist**.

- I created it for myself and use it to manage my Rebrickable inventory. I've never had a problem, but you never know.

- If a file is corrupted or contains incorrect quantities, **it may affect your collection data**.

- So far, all internal tests have passed successfully, but caution is recommended when using the outputs in production.

---

## 🤝 Contact:
For issues, suggestions, or contributions, feel free to open an issue on the GitHub repository.

---

> Created for LEGO enthusiasts who want fast, dependency-free manipulation of BrickLink XML inventories.
