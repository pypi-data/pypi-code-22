import os
import time
import logging
import click

from osmtogtfs.osm_processor import GTFSPreprocessor
from osmtogtfs.gtfs_writer import GTFSWriter
from osmtogtfs.gtfs_dummy import populate_dummy_data


@click.command()
@click.argument('osmfile', type=click.Path(exists=True, readable=True))
@click.option('--outdir', default='.',
              type=click.Path(exists=True,
                              dir_okay=True,
                              writable=True,
                              resolve_path=True),
              help='Output directory. Default is the current directory.')
@click.option('--zipfile',
              type=click.Path(file_okay=True,
                              writable=True,
                              resolve_path=True),
              help='Save to zipfile. Default is saving to flat text files.')
@click.option('--dummy/--no-dummy',
              default=False,
              help='Whether to fill the missing parts with dummy data.')
def cli(osmfile, outdir, zipfile, dummy):
    processor = GTFSPreprocessor()
    start = time.time()
    processor.apply_file(osmfile, locations=True, idx='sparse_mem_array')
    logging.debug("Preprocessing took %d seconds.", (time.time() - start))

    writer = GTFSWriter()
    writer.add_agencies(processor.agencies.values())
    writer.add_stops(processor.stops.values())
    writer.add_routes(processor.routes.values())
    writer.add_shapes(processor.shapes)

    if dummy:
        populate_dummy_data(writer, processor)

    if zipfile:
        writer.write_zipped(os.path.join(outdir, zipfile))
        click.echo('GTFS feed saved in %s' % zipfile)
    else:
        writer.write_unzipped(outdir)
        click.echo('GTFS feed saved in %s' % outdir)
