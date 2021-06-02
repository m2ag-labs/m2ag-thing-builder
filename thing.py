from __future__ import division, print_function

import logging
import time
import os.path
from pathlib import Path

from webthing import (MultipleThings, WebThingServer)
from device.services.services import Services
from device.things.things import Things
from api.helpers.config import Config

config = Config.get_server_config()


def run_server():
    # check to see if server.crt and .key are available
    if os.path.isfile(f'{str(Path.home())}/.m2ag-labs/ssl/server.crt') \
            and os.path.isfile(f'{str(Path.home())}/.m2ag-labs/ssl/server.crt'):
        ssl_options = {
            'certfile': f'{str(Path.home())}/.m2ag-labs/ssl/server.crt',
            'keyfile': f'{str(Path.home())}/.m2ag-labs/ssl/server.key',
        }
    else:
        ssl_options = None

    device = Services(config, logging)
    things = Things(config, logging, device.components)
    server = WebThingServer(MultipleThings(things.things, config['thing_server']),
                            port=8888, ssl_options=ssl_options)

    time.sleep(5)  # allow webthing to start before advertising

    logging.info('starting the server')
    # TODO: add extra advertising or turn off here
    server.start()
    # noinspection PyBroadException
    """try:
        # TODO: fix this up 
    except:
        # TODO: Add clean up code
        # logging.debug('canceling the sensor update looping task')
        # sensor.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')"""


if __name__ == '__main__':
    logging.basicConfig(
        level=config['log_level'],
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
