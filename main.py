from game import campaign, common as cu, dark_forest, ending, heroes, ranhorn
from utils import constant, handler_adb, handler_config, handler_cv2

# Init everything
# _cfg = handler_config.HandlerConfig("config/config.ini")
# _cfg.init()

_adb = handler_adb.HandlerAdb()
_adb.init()
# _adb.start(constant.PACKAGE_NAME, 0)

_cv2 = handler_cv2.HandlerCv2(_adb)
_cv2.dev()
_cv2.show_debug_image = True

# First things first
_game_common = cu.Common(_cv2)
_game_common.run()

# Campaign tab
_game_campaign = campaign.Campaign(_cv2)
# _game_campaign.run()

# Dark Forest
# _game_dark_forest = dark_forest.DarkForest(_cv2)
# _game_dark_forest.run()

# Ranhorn
# _game_ranhorn = ranhorn.Ranhorn(_cv2)
# _game_ranhorn.run()

# Heroes
# _game_heroes = heroes.Heroes(_cv2)
# _game_heroes.run()

# End
# _game_ending = ending.Ending(_cv2)
# _game_after.run()
