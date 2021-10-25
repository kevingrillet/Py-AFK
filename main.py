from game import common_utils as cu, tab_global as glob, tab_heroes as heroes, tab_ranhorn as ranhorn, \
    tab_campaign as campaign, tab_dark_forest as dark_forest
from utils import handler_adb as adb, handler_config as cfg, handler_cv2 as cv2, constant

_cfg = cfg.HandlerConfig("config/config.ini")
_cfg.init()

_adb = adb.HandlerAdb()
_adb.init()
_adb.start(constant.PACKAGE_NAME, 0)

_cv2 = cv2.HandlerCv2(_adb)
_cv2.dev()


def game_starting():
    # First things first
    _cu = cu.CommonUtils(_cv2)
    _cu.wait_game_to_load()
    _cu.wait_update()
    _cu.close_main_menu_popup()


def game_daily():
    # Campaign tab
    campaign.collect_loot()
    campaign.battle()
    campaign.fast_rewards()
    campaign.collect_loot()

    # Dark Forest
    dark_forest.kings_tower()
    dark_forest.arena_of_heroes()
    dark_forest.bounty_board()

    # Ranhorn
    ranhorn.guild()
    ranhorn.the_oak_inn()
    ranhorn.temple_of_ascension()
    ranhorn.resonating_crystal()
    ranhorn.the_noble_tavern()
    ranhorn.store()

    # Heroes
    heroes.enhance_gear()

    # End
    glob.quests()
    glob.marchants()
    glob.mail()


if False:
    game_starting()
    game_daily()
