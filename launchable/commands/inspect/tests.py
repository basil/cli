import click
import os
from ...utils.env_keys import REPORT_ERROR_KEY
from ...utils.http_client import LaunchableClient
from tabulate import tabulate


@click.command()
@click.option(
    '--test-session-id',
    'test_session_id',
    help='test session id',
    required=True
)
def tests(test_session_id):
    try:
        client = LaunchableClient()
        res = client.request(
            "get", "/test_sessions/{}/events".format(test_session_id))
        res.raise_for_status()
        results = res.json()
    except Exception as e:
        if os.getenv(REPORT_ERROR_KEY):
            raise e
        else:
            click.echo(e, err=True)
        click.echo(click.style(
            "Warning: the failed to inspect tests", fg='yellow'),
            err=True)

        return

    header = ["Test Path",
              "Estimated duration (sec)", "Status", "Stdout", "Stderr", "Uploaded At"]

    rows = [["#".join([path["type"] + "=" + path["name"] for path in result["testPath"]]),
             "{:0.4f}".format(result["duration"]), result["status"], result["stdout"], result["stderr"], result["createdAt"]] for result in results]

    click.echo(tabulate(rows, header, tablefmt="github"))
