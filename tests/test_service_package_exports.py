"""Validate the public surface declared by each service package."""

import ast
import unittest
from pathlib import Path

PACKAGE_EXPORTS = {
    "alarm": ["AlarmClient"],
    "artifact": ["ArtifactClient"],
    "assetmanagement": ["AssetManagementClient"],
    "dataframe": ["DataFrameClient"],
    "feeds": ["FeedsClient"],
    "file": ["FileClient"],
    "notebook": ["NotebookClient"],
    "notification": ["NotificationClient"],
    "product": ["ProductClient"],
    "spec": ["SpecClient"],
    "systems": ["SystemsClient"],
    "tag": [
        "DataType",
        "RetentionType",
        "TagData",
        "TagWithAggregates",
        "AsyncTagQueryResultCollection",
        "ITagReader",
        "ITagWriter",
        "BufferedTagWriter",
        "TagValueReader",
        "TagValueWriter",
        "TagUpdateFields",
        "TagDataUpdate",
        "TagPathUtilities",
        "TagQueryResultCollection",
        "TagSubscription",
        "TagSelection",
        "TagManager",
    ],
    "test_plan": ["TestPlanClient"],
    "testmonitor": ["TestMonitorClient"],
    "work_item": ["WorkItemClient", "WorkItemExecuteApiException"],
}


class TestServicePackageExports(unittest.TestCase):
    """Verify service package docstrings and explicit export lists."""

    def test_service_package_exports_are_explicit(self):
        """Each service package should document and declare its public exports."""
        package_root = Path(__file__).resolve().parents[1] / "nisystemlink" / "clients"

        for package_name, exported_names in PACKAGE_EXPORTS.items():
            with self.subTest(package_name=package_name):
                module_path = package_root / package_name / "__init__.py"
                module = ast.parse(module_path.read_text(encoding="utf-8"))
                imported_names = []
                declared_exports = None
                module_docstring = ast.get_docstring(module)

                self.assertIsNotNone(module_docstring)
                if module_docstring is None:
                    self.fail(f"Missing module docstring in {module_path}")
                self.assertTrue(module_docstring.startswith("Start here with "))

                for node in module.body:
                    if isinstance(node, ast.ImportFrom):
                        imported_names.extend(alias.name for alias in node.names)
                    elif isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == "__all__":
                                declared_exports = ast.literal_eval(node.value)

                self.assertEqual(declared_exports, exported_names)
                self.assertCountEqual(imported_names, exported_names)
