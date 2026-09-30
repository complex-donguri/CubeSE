import os
import unittest
from pathlib import Path
from unittest.mock import patch

import cubese_runtime


class RuntimePathTests(unittest.TestCase):
    def test_image_path_is_relative_to_application(self) -> None:
        self.assertEqual(
            cubese_runtime.image_path("U"),
            cubese_runtime.APPLICATION_DIRECTORY / "RP" / "U.png",
        )

    def test_engine_override_is_resolved(self) -> None:
        configured = Path("build") / "custom-cubese-engine"
        with patch.dict(os.environ, {"CUBESE_ENGINE": str(configured)}):
            self.assertEqual(cubese_runtime.engine_path(), configured.resolve())

    def test_engine_environment_preserves_override(self) -> None:
        with patch.dict(os.environ, {"CUBESE_DATA_DIR": "custom-data"}):
            environment = cubese_runtime.engine_environment()
        self.assertEqual(environment["CUBESE_DATA_DIR"], "custom-data")

    def test_engine_environment_defaults_to_application_directory(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            environment = cubese_runtime.engine_environment()
        self.assertEqual(
            environment["CUBESE_DATA_DIR"],
            str(cubese_runtime.APPLICATION_DIRECTORY),
        )


if __name__ == "__main__":
    unittest.main()
