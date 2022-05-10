import logging
import sys
import time
from datetime import datetime
from pathlib import Path

from game import campaign, common as gc, constant as gcst
from utils import constant, handleradb, handlercv2, common, handlerconfig


def load_config():
    """
    Load config from config file
    Create it if not existing
    :return:
    """
    hcfg = handlerconfig.HandlerConfig('config/config.ini')
    gcst.DEBUG_LEVEL = constant.DebugLevel(int(hcfg.get_value('debug', str(gcst.DEBUG_LEVEL.value), 'Settings')))
    gcst.DEV_MODE = hcfg.get_value('dev', str(gcst.DEV_MODE), 'Settings') == 'True'
    gcst.SCALE = float(hcfg.get_value('scale', str(gcst.SCALE), 'Settings'))


if __name__ == '__main__':
    try:
        # Setup everything for the script
        Path('logs/').mkdir(parents=True, exist_ok=True)
        logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout),
                                      logging.FileHandler('logs/' + str(datetime.now()).replace(':', '.') + '.log')],
                            format='%(message)s', level=logging.DEBUG)
        common.info('Started')
        start_time = time.time()
        load_config()

        # Start ADB Handler (find ADB, start APP)
        hadb = handleradb.HandlerAdb(scale=gcst.SCALE)
        hadb.init()
        hadb.start(constant.PACKAGE_NAME, 0)

        # Start CV2 Handler (set ADB to get Screenshots, set scale)
        hcv2 = handlercv2.HandlerCv2(hadb, scale=gcst.SCALE)
        hcv2.dev()  # Dev mod to take screenshots with adb + cv2
        hcv2.threshold = 0.9 if gcst.SCALE == 1 else 0.8

        # Wait for the app to start, update, ... after this step, should be in game.
        gc.Common(hcv2).run()

        # Real code start here.
        campaign.Campaign(hcv2).run()

        common.info('Done')

    except Exception as e:
        log = logging.getLogger()
        for hdlr in log.handlers[:]:  # remove the existing file handlers
            if not isinstance(hdlr, logging.FileHandler):
                log.removeHandler(hdlr)
        handler = logging.StreamHandler(sys.stderr)
        log.addHandler(handler)
        logging.error(e, exc_info=True)
