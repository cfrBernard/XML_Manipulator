## [v1.4.0] - 2025-11-17

### Feature

Add `merge` command to automatically merge multiple XML files from a folder into a single inventory file. Duplicate items are combined by summing their quantities. Supports `--dry-run` and `--verbose` options.

---

## [v1.3.0] - 2025-11-17

### Feature

Log coloring: make [INFO], [OK], [DRY] and [ERROR] visually distinct for better readability

---

## [v1.2.0] - 2025-11-14

### Feature

Now show how many colors are present in the inventory via the "stats" command.

---

## [v1.1.0] - 2025-11-13

### Feature

You can now use the relative or absolute path for `--input`. Useful if your `.xml` file is not in the `input/` folder:

```
--input parts.xml (If it is in assets/input/)

OR

--input assets/input/parts.xml
```

---
