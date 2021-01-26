import os

import click

from . import launchable


@click.option(
    '--enable-format',
    'enable_format',
    is_flag=True,
    help='print with `--tests ` flag'
)
@click.argument('source_roots', required=True, nargs=-1)
@launchable.subset
def subset(client, source_roots, enable_format):
    def file2test(f: str):
        if f.endswith('.java') or f.endswith('.scala') or f.endswith('.kt'):
            f = f[:f.rindex('.')]   # remove extension
            # directory -> package name conversion
            cls_name = f.replace(os.path.sep, '.')
            return [{"type": "class", "name": cls_name}]
        else:
            return None

    for root in source_roots:
        client.scan(root, '**/*', file2test)

    if enable_format:
        client.formatter = lambda x: "--tests {}".format(x[0]['name'])
        client.separator = ' '

    client.run()


record_tests = launchable.CommonRecordTestImpls(__name__).report_files()
