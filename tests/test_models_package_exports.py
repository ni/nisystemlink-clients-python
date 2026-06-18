"""Validate the public surface declared by each models package."""

import ast
import unittest
from pathlib import Path


class TestModelsPackageExports(unittest.TestCase):
    """Verify models package export lists are explicit and complete."""

    def test_models_package_exports_are_explicit(self):
        """Each models package should declare an explicit __all__ export list."""
        clients_root = Path(__file__).resolve().parents[1] / "nisystemlink" / "clients"
        model_init_files = sorted(clients_root.glob("*/models/__init__.py"))

        self.assertGreater(len(model_init_files), 0)

        for module_path in model_init_files:
            with self.subTest(module_path=str(module_path)):
                module = ast.parse(module_path.read_text(encoding="utf-8"))
                exported_names = []
                seen = set()
                declared_exports = None

                for node in module.body:
                    if isinstance(node, ast.ImportFrom):
                        for alias in node.names:
                            name = alias.asname or alias.name
                            if not name.startswith("_") and name not in seen:
                                seen.add(name)
                                exported_names.append(name)
                    elif isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == "__all__":
                                declared_exports = ast.literal_eval(node.value)
                            elif (
                                isinstance(target, ast.Name)
                                and not target.id.startswith("_")
                                and target.id not in seen
                            ):
                                seen.add(target.id)
                                exported_names.append(target.id)

                self.assertIsNotNone(declared_exports)
                if declared_exports is None:
                    self.fail(f"Missing __all__ in {module_path}")

                self.assertEqual(declared_exports, exported_names)
