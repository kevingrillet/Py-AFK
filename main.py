from game import common_utils as cu, tab_global as glob, tab_heroes as heroes, tab_ranhorn as ranhorn, \
    tab_campaign as campaign, tab_dark_forest as dark_forest
from utils import handler_adb as adb, handler_config as cfg, constant


def check_adb():
    adb.check()  # Installing ADB
    adb.restart()  # Starting ADB
    if not adb.connect():
        print("[ERROR] Failed to connect to ADB.")
        exit(1)
    print(adb.get_resolution())  # Get resolution
    adb.stop_app(constant.PACKAGE_NAME)  # Stop the app
    adb.start_app(constant.PACKAGE_NAME, 30)  # Start the app


def check_config():
    config = cfg.get("config/config.ini")
    if not config:
        print("[ERROR] No config found.")


def game_starting():
    # First things first
    cu.wait_game_to_load()
    cu.wait_update()
    cu.close_main_menu_popup()


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


check_config()
check_adb()

adb.dev()

if False:
    game_starting()
    game_daily()
