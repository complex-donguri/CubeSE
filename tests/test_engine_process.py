import io
import unittest
from unittest.mock import MagicMock, patch

import cubese_process


class EngineProcessTests(unittest.TestCase):
    def test_legacy_command_keeps_move_apostrophes(self) -> None:
        self.assertEqual(
            cubese_process.legacy_command_arguments("CubeSE.exe 0 R' U2"),
            ["0", "R'", "U2"],
        )

    def test_empty_legacy_command_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            cubese_process.legacy_command_arguments("   ")

    @patch("cubese_process.subprocess.Popen")
    @patch("cubese_process.engine_environment")
    @patch("cubese_process.engine_path")
    def test_start_engine_uses_argument_list_and_environment(
        self,
        mocked_engine_path: MagicMock,
        mocked_environment: MagicMock,
        mocked_popen: MagicMock,
    ) -> None:
        mocked_engine_path.return_value = "/application/CubeSE"
        mocked_environment.return_value = {"CUBESE_DATA_DIR": "/application"}

        cubese_process.start_engine("CubeSE.exe 1 2 3")

        command = mocked_popen.call_args.args[0]
        options = mocked_popen.call_args.kwargs
        self.assertEqual(command, ["/application/CubeSE", "1", "2", "3"])
        self.assertFalse(options["shell"])
        self.assertTrue(options["text"])
        self.assertEqual(options["encoding"], "utf-8")
        self.assertEqual(options["env"]["CUBESE_DATA_DIR"], "/application")

    def test_iter_engine_output_removes_line_endings(self) -> None:
        process = MagicMock()
        process.stdout = io.StringIO("first\r\nsecond\n")
        self.assertEqual(
            list(cubese_process.iter_engine_output(process)),
            ["first", "second"],
        )


if __name__ == "__main__":
    unittest.main()
