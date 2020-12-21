import click
import types
from launchable.commands.optimize.tests import tests as optimize_tests_cmd
from launchable.commands.record.tests import tests as record_tests_cmd


def cmdname(f):
    """figure out the sub-command name from a test runner function"""

    # a.b.cde -> cde
    m = f.__module__
    return m[m.rindex('.')+1:]


def wrap(f, group):
    """
    Wraps a 'plugin' function into a click command and registers it to the given group.

    a plugin function receives the scanner object in its first argument
    """
    d = click.command(name=cmdname(f))
    cmd = d(click.pass_obj(f))
    group.add_command(cmd)
    return cmd


optimize = types.SimpleNamespace()
optimize.tests = lambda f: wrap(f, optimize_tests_cmd)

record = types.SimpleNamespace()
record.tests = lambda f: wrap(f, record_tests_cmd)