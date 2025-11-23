# Usage

The tool is a single CLI script: `app.py`. It provides three main commands: `stats`, `split` and `merge`.

## General Help

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

---

## 1. Stats

Show basic statistics about your BrickLink inventory.

### Command:

```
python app.py stats --input parts.xml
```

### Output example:

```
[INFO] Total physical pieces: 42817
[INFO] Unique items: 1342
[INFO] Different colors: 36
```

---

## 2. Split 

Split your inventory XML into multiple files, based on unique parts or by grouping items per color.

### Classic split command:

```
python app.py split --input parts.xml --max 1000 --verbose
```

### By-color split command:

```
python app.py split --input parts.xml --max 1000 --verbose --bycolor
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
python app.py split --input parts.xml --max 1000 --dry-run --verbose
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

---

## 3. Merge

Merge multiple XML files into a single inventory file. By default, it merges all XML files in `assets/input/merge/`.

### Command:

```
python app.py merge --verbose
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