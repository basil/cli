from pathlib import Path
from unittest import mock
import responses  # type: ignore
import json
import gzip
from tests.cli_test_case import CliTestCase
from launchable.utils.http_client import get_base_url


class AntTest(CliTestCase):
    test_files_dir = Path(__file__).parent.joinpath(
        '../data/ant/').resolve()

    @responses.activate
    def test_subset(self):
        result = self.cli('subset', '--target', '10%', '--session',
                          self.session, 'ant', str(self.test_files_dir.joinpath('src').resolve()))
        self.assertEqual(result.exit_code, 0)

        payload = json.loads(gzip.decompress(
            responses.calls[0].request.body).decode())

        expected = self.load_json_from_file(
            self.test_files_dir.joinpath('subset_result.json'))

        self.assert_json_orderless_equal(expected, payload)

    @ responses.activate
    def test_record_test_maven(self):
        result = self.cli('record', 'tests',  '--session', self.session,
                          'ant', str(self.test_files_dir) + "/junitreport/TESTS-TestSuites.xml")
        self.assertEqual(result.exit_code, 0)

        payload = json.loads(gzip.decompress(
            b''.join(responses.calls[1].request.body)).decode())

        def removeDate(data):
            for e in data["events"]:
                del e["created_at"]

        expected = self.load_json_from_file(
            self.test_files_dir.joinpath("record_test_result.json"))

        removeDate(payload)
        removeDate(expected)

        self.assert_json_orderless_equal(expected, payload)
