"""Subcommand for importing translations."""

import os
import click
from grow.commands import shared
from grow.pods import pods
from grow.pods import storage


@click.command()
@shared.pod_path_argument
@click.option('--source', type=click.Path(), required=True,
              help='Path to source (either zip file, directory, or file).')
@click.option('--locale', type=str,
              help='Locale of the message catalog to import. This option is'
                   ' only applicable when --source is a .po file.')
@click.option('--include-obsolete/--no-include-obsolete',
              default=True,
              help='Whether to include potentially obsolete messages or just'
                   ' include translations for strings that already exist in'
                   ' catalogs.')
def import_translations(pod_path, source, locale, include_obsolete):
    """Imports translations from an external source."""
    if source.endswith('.po') and locale is None:
        text = 'Must specify --locale when --source is a .po file.'
        raise click.ClickException(text)
    if not source.endswith('.po') and locale is not None:
        text = 'Cannot specify --locale when --source is not a .po file.'
        raise click.ClickException(text)
    source = os.path.expanduser(source)
    root = os.path.abspath(os.path.join(os.getcwd(), pod_path))
    pod = pods.Pod(root, storage=storage.FileStorage)
    if not pod.exists:
        raise click.ClickException('Pod does not exist: {}'.format(pod.root))
    with pod.profile.timer('grow_import_translations'):
        pod.catalogs.import_translations(
            source, locale=locale, include_obsolete=include_obsolete)
    return pod
