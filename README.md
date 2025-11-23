# XML_Manipulator

![Version](https://img.shields.io/badge/version-v1.6.1-blue)
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

## Quickstart

```
python app.py stats --input parts.xml
python app.py split --input parts.xml --max 1000
```

> These commands expect your input file in `assets/input/`.  
> The output files will appear in `assets/output/<timestamp>/`.

---

## Commands Overview

The tool provides three main commands: **stats**, **split** and **merge**.

- `stats` – Get inventory statistics  
- `split` – Split by unique parts or by color  
- `merge` – Merge multiple XML inventories  

> Full command examples in the [USAGE](docs/USAGE.md) file.

---

## Notes:

- `--input` path can be absolute or relative.
- `--dry-run` does not create files.
- Output folders use timestamps and are never overwritten.
- For more information about the version, please refer to the [changelog](docs/CHANGELOG.md) section.
- This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
- More details in the [FAQ](docs/FAQ.md).

---

## ⚠️ Disclaimer

- This tool is provided **as-is**. While it has been tested on multiple inventories, **bugs may still exist**.
- If a file is corrupted or contains incorrect quantities, **it may affect your collection data**. 

> Caution is recommended when using the outputs in production.

---

## What's Coming:

- Export CSV: generate a CSV with part IDs, colors, and quantities
- Filter options: split or analyze by part type, or custom filters
- Desktop interface

---

## Contact:
For issues, suggestions, or contributions, feel free to open an issue on the GitHub repository.

---

> Created for LEGO enthusiasts who want fast, dependency-free manipulation of BrickLink XML inventories.
