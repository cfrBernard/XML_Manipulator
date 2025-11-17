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


def main():
    parser = argparse.ArgumentParser(description="XML Manipulator for BrickLink inventories")
    sub = parser.add_subparsers(dest="cmd")

    # stats
    p_stats = sub.add_parser("stats", help="Show stats about an XML inventory")
    p_stats.add_argument("--input", required=True)

    # split
    p_split = sub.add_parser("split", help="Split an XML into chunks of unique parts")
    p_split.add_argument("--input", required=True)
    p_split.add_argument("--max", type=int, default=1000)
    p_split.add_argument("--dry-run", action="store_true")
    p_split.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    # Input path management (v1.1.0)
    if os.path.isabs(args.input) or os.path.exists(args.input):
        input_path = args.input
    else:
        input_path = os.path.join("assets", "input", args.input)

    # stats
    if args.cmd == "stats":
        tree = load_xml(input_path)
        unique, total_qty, colors_set = compute_stats(tree)
        Log.info(f"Total physical pieces: {total_qty}")
        Log.info(f"Unique items: {len(unique)}")
        Log.info(f"Different colors: {len(colors_set)}")
        return

    # split
    if args.cmd == "split":
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

    parser.print_help()


if __name__ == "__main__":
    main()
