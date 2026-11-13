import argparse
import json
from pathlib import Path
import tempfile

import osmium


ROOT = Path(__file__).resolve().parent.parent


def traffic_sign_value(sign):
    values = [tag["traffic_sign"] for tag in sign["tags"] if "traffic_sign" in tag]
    if len(values) != 1:
        raise ValueError("Each sign definition must contain exactly one traffic_sign tag")
    return values[0]


def count_frequencies(pbf_path, values):
    """Count exact traffic_sign values on nodes, ways and relations in one pass."""
    counts = dict.fromkeys(values, 0)
    # Filter in libosmium before entering Python. No geometry/location cache is needed.
    objects = osmium.FileProcessor(pbf_path).with_filter(
        osmium.filter.KeyFilter("traffic_sign")
    )
    for obj in objects:
        value = obj.tags["traffic_sign"]
        if value in counts:
            counts[value] += 1
    return counts


def update_frequencies(pbf_path, definitions_path):
    with definitions_path.open(encoding="utf-8") as f:
        signs = json.load(f)
    values = [traffic_sign_value(next(iter(item.values()))) for item in signs]

    # Finish reading the entire extract before changing any definitions.
    counts = count_frequencies(pbf_path, values)
    for item, value in zip(signs, values):
        key, sign = next(iter(item.items()))
        sign["frequency"] = counts[value]
        print(f"{key} - {counts[value]}")
    signs.sort(key=lambda item: next(iter(item.values()))["frequency"], reverse=True)

    # Replace atomically so a failed run leaves the previous definitions intact.
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=definitions_path.parent, delete=False
        ) as f:
            temporary_path = Path(f.name)
            json.dump(signs, f, indent=4)
        temporary_path.replace(definitions_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description="Sort sign definitions by frequency in a local Geofabrik Germany extract."
    )
    parser.add_argument(
        "pbf", nargs="?", type=Path, default=ROOT / "data/germany-latest.osm.pbf",
        help="Local OSM PBF file (default: data/germany-latest.osm.pbf in the repository)",
    )
    args = parser.parse_args()
    if not args.pbf.is_file():
        parser.error(f"PBF file not found: {args.pbf}. Download the Geofabrik extract first (see README).")
    print(f"Counting traffic_sign values in {args.pbf}", flush=True)
    update_frequencies(args.pbf, ROOT / "definitions/signs.json")


if __name__ == "__main__":
    main()
