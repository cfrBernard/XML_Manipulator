import argparse
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

from scripts.utils.log import Log


def load_xml(path):
    try:
        tree = ET.parse(path)
        return tree
    except Exception as e:
        Log.error(f"Unable to load XML {path}: {e}")
        sys.exit(1)


def compute_stats(tree):
    root = tree.getroot()
    unique = defaultdict(int)
    total_qty = 0
    colors_set = set()

    for item in root.findall("ITEM"):
        part = item.findtext("ITEMID", default="?")
        color = item.findtext("COLOR", default="?")
        qty = int(item.findtext("QTY", default="0"))
        unique[(part, color)] += qty
        total_qty += qty
        colors_set.add(color)

    return unique, total_qty, colors_set


def split_xml(tree, max_unique, outdir, dry_run=False, verbose=False):
    root = tree.getroot()
    unique = {}

    # First group unique items
    for item in root.findall("ITEM"):
        part = item.findtext("ITEMID", default="?")
        color = item.findtext("COLOR", default="?")
        key = (part, color)
        if key not in unique:
            unique[key] = item
        else:
            # Merge quantities for safety
            q1 = int(unique[key].findtext("QTY", default="0"))
            q2 = int(item.findtext("QTY", default="0"))
            unique[key].find("QTY").text = str(q1 + q2)

    all_items = list(unique.values())
    chunks = [all_items[i : i + max_unique] for i in range(0, len(all_items), max_unique)]

    if verbose:
        Log.info(f"Total unique items: {len(all_items)}")
        Log.info(f"Will generate {len(chunks)} files.")

    # Prepare output dir
    if not dry_run:
        os.makedirs(outdir, exist_ok=True)

    outputs = []
    for i, chunk in enumerate(chunks, start=1):
        new_root = ET.Element("INVENTORY")
        for item in chunk:
            new_root.append(item)

        tree_out = ET.ElementTree(new_root)
        outpath = os.path.join(outdir, f"output_{i}.xml")
        outputs.append(outpath)

        if dry_run:
            if verbose:
                Log.dry(f"Would write: {outpath}")
        else:
            tree_out.write(outpath, encoding="utf-8", xml_declaration=True)
            if verbose:
                Log.ok(f"Wrote {outpath}")

    return outputs


def merge_xml(input_dir, out_path, verbose=False, dry_run=False):
    """Merge all XML files in a directory into a single XML."""
    all_items = {}

    xml_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".xml")]
    if verbose:
        Log.info(f"Found {len(xml_files)} XML files in {input_dir}")

    for xml_file in xml_files:
        path = os.path.join(input_dir, xml_file)
        tree = load_xml(path)
        root = tree.getroot()

        for item in root.findall("ITEM"):
            part = item.findtext("ITEMID", default="?")
            color = item.findtext("COLOR", default="?")
            key = (part, color)

            if key in all_items:
                q_existing = int(all_items[key].findtext("QTY", default="0"))
                q_new = int(item.findtext("QTY", default="0"))
                all_items[key].find("QTY").text = str(q_existing + q_new)
            else:
                all_items[key] = item

    new_root = ET.Element("INVENTORY")
    for item in all_items.values():
        new_root.append(item)

    tree_out = ET.ElementTree(new_root)

    if dry_run:
        Log.dry(f"Would write merged file to: {out_path}")
    else:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        tree_out.write(out_path, encoding="utf-8", xml_declaration=True)
        if verbose:
            Log.ok(f"Merged XML written to: {out_path}")

    return out_path


def main():
    parser = argparse.ArgumentParser(description="XML Manipulator for BrickLink inventories")
    sub = parser.add_subparsers(dest="cmd")

    # ===== stats =====
    p_stats = sub.add_parser("stats", help="Show stats about an XML inventory")
    p_stats.add_argument("--input", required=True)

    # ===== split =====
    p_split = sub.add_parser("split", help="Split an XML into chunks of unique parts")
    p_split.add_argument("--input", required=True)
    p_split.add_argument("--max", type=int, default=1000)
    p_split.add_argument("--dry-run", action="store_true")
    p_split.add_argument("--verbose", action="store_true")

    # ===== merge =====
    p_merge = sub.add_parser("merge", help="Merge all XML files in a folder into one")
    p_merge.add_argument(
        "--input-dir",
        default=os.path.join("assets", "input", "merge"),
        help="Directory containing XML files to merge (default: assets/input/merge/)"
    )
    p_merge.add_argument(
        "--output",
        default=os.path.join("assets", "output", f"merged_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xml"),
        help="Output path for merged XML"
    )
    p_merge.add_argument("--dry-run", action="store_true")
    p_merge.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    # ===== stats =====
    if args.cmd == "stats":
        input_path = args.input if os.path.isabs(args.input) or os.path.exists(args.input) else os.path.join("assets", "input", args.input)
        tree = load_xml(input_path)
        unique, total_qty, colors_set = compute_stats(tree)
        Log.info(f"Total physical pieces: {total_qty}")
        Log.info(f"Unique items: {len(unique)}")
        Log.info(f"Different colors: {len(colors_set)}")
        return

    # ===== split =====
    if args.cmd == "split":
        input_path = args.input if os.path.isabs(args.input) or os.path.exists(args.input) else os.path.join("assets", "input", args.input)
        date_dir = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        outdir = os.path.join("assets", "output", date_dir)
        tree = load_xml(input_path)
        outputs = split_xml(
            tree,
            args.max,
            outdir,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )
        if not args.dry_run:
            Log.info(f"Generated {len(outputs)} files in {outdir}")
        return

    # ===== merge =====
    if args.cmd == "merge":
        input_dir = args.input_dir if os.path.isabs(args.input_dir) or os.path.exists(args.input_dir) else os.path.join("assets", "input", args.input_dir)
        merge_xml(
            input_dir=input_dir,
            out_path=args.output,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
