import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import osmium


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sort_values", ROOT / "scripts/sort-values.py")
sort_values = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sort_values)


def definition(key, value):
    return {key: {"tags": [{"traffic_sign": value}], "frequency": 999, "cat": 1}}


class FrequencyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.pbf = self.directory / "sample.osm.pbf"
        self.definitions = self.directory / "signs.json"
        with osmium.SimpleWriter(str(self.pbf)) as writer:
            writer.add_node(osmium.osm.mutable.Node(
                id=1, location=(13, 51), tags={"traffic_sign": "DE:237"}
            ))
            writer.add_node(osmium.osm.mutable.Node(
                id=2, location=(13, 51), tags={"traffic_sign:forward": "DE:237"}
            ))
            writer.add_node(osmium.osm.mutable.Node(id=3, location=(13, 51)))
            writer.add_node(osmium.osm.mutable.Node(
                id=4, location=(13, 51), tags={"traffic_sign": "DE:237;DE:239"}
            ))
            writer.add_node(osmium.osm.mutable.Node(
                id=5, location=(13, 51), tags={"traffic_sign": "DE:239;DE:237"}
            ))
            writer.add_node(osmium.osm.mutable.Node(
                id=6, location=(13, 51), tags={"traffic_sign": "DE:237,1022-10"}
            ))
            writer.add_node(osmium.osm.mutable.Node(
                id=7, location=(13, 51), tags={"traffic_sign": "DE:237 "}
            ))
            writer.add_way(osmium.osm.mutable.Way(
                id=1, nodes=[1, 2], tags={"traffic_sign": "DE:237"}
            ))
            writer.add_relation(osmium.osm.mutable.Relation(
                id=1, members=[("w", 1, "")], tags={"traffic_sign": "DE:237"}
            ))

    def update(self):
        with contextlib.redirect_stdout(io.StringIO()):
            sort_values.update_frequencies(self.pbf, self.definitions)

    def test_counts_all_object_types_and_exact_values(self):
        self.assertEqual(
            sort_values.count_frequencies(self.pbf, [
                "DE:237", "DE:239", "DE:237;DE:239", "DE:237,1022-10", "DE:237"
            ]),
            {"DE:237": 3, "DE:239": 0, "DE:237;DE:239": 1, "DE:237,1022-10": 1},
        )

    def test_sort_preserves_metadata_duplicates_and_tie_order(self):
        entries = [definition("absent", "DE:239"), definition("combo", "DE:237;DE:239"),
                   definition("common", "DE:237"), definition("same-value", "DE:237")]
        self.definitions.write_text(json.dumps(entries), encoding="utf-8")
        self.update()
        result = json.loads(self.definitions.read_text(encoding="utf-8"))
        self.assertEqual([next(iter(entry)) for entry in result],
                         ["common", "same-value", "combo", "absent"])
        expected = {next(iter(entry)): next(iter(entry.values())) for entry in entries}
        for entry in result:
            key, value = next(iter(entry.items()))
            expected[key]["frequency"] = {"common": 3, "same-value": 3, "combo": 1, "absent": 0}[key]
            self.assertEqual(value, expected[key])

    def test_missing_or_truncated_pbf_preserves_definitions(self):
        original = json.dumps([definition("common", "DE:237")]).encode()
        self.definitions.write_bytes(original)
        self.pbf.unlink()
        with self.assertRaises((OSError, RuntimeError)):
            self.update()
        self.assertEqual(self.definitions.read_bytes(), original)

        # A valid header and data followed by an incomplete blob must fail,
        # even if the reader has already seen some matching objects.
        with osmium.SimpleWriter(str(self.pbf)) as writer:
            writer.add_node(osmium.osm.mutable.Node(
                id=1, location=(13, 51), tags={"traffic_sign": "DE:237"}
            ))
        with self.pbf.open("ab") as f:
            f.write(b"\x00\x00\x00\x20truncated")
        with self.assertRaises((OSError, RuntimeError)):
            self.update()
        self.assertEqual(self.definitions.read_bytes(), original)

    def test_invalid_definition_preserves_file(self):
        entries = [definition("common", "DE:237"), {"missing": {"tags": [], "frequency": 999}}]
        self.definitions.write_text(json.dumps(entries), encoding="utf-8")
        original = self.definitions.read_bytes()
        with self.assertRaises(ValueError):
            self.update()
        self.assertEqual(self.definitions.read_bytes(), original)

    def test_cli_works_from_repository_and_scripts_directory(self):
        (self.directory / "scripts").mkdir()
        (self.directory / "definitions").mkdir()
        (self.directory / "data").mkdir()
        script = self.directory / "scripts/sort-values.py"
        shutil.copy(ROOT / "scripts/sort-values.py", script)
        shutil.copy(self.pbf, self.directory / "data/germany-latest.osm.pbf")
        definitions = self.directory / "definitions/signs.json"
        for cwd, args in [(self.directory, [str(self.pbf)]), (script.parent, [])]:
            with self.subTest(cwd=cwd):
                definitions.write_text(json.dumps([definition("common", "DE:237")]), encoding="utf-8")
                subprocess.run([sys.executable, str(script), *args], cwd=cwd,
                               capture_output=True, text=True, check=True)
                self.assertEqual(json.loads(definitions.read_text())[0]["common"]["frequency"], 3)
        original = definitions.read_bytes()
        result = subprocess.run([sys.executable, str(script), "missing.osm.pbf"],
                                cwd=self.directory, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PBF file not found", result.stderr)
        self.assertEqual(definitions.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
