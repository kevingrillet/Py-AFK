from game import game_utils as gu, game_logic as gl
from utils import handler_adb as adb, handler_config as cfg


def check_adb():
    adb.check()  # Installing ADB
    adb.restart()  # Starting ADB
    if not adb.connect():
        print("[ERROR] Failed to connect to ADB.")
        exit(1)
    print(adb.get_resolution())  # Get resolution
    adb.stop_app("com.lilithgame.hgame.gp")  # Stop the app
    adb.start_app("com.lilithgame.hgame.gp", 30)  # Start the app


def check_config():
    config = cfg.get("config/config.ini")
    if not config:
        print("[ERROR] No config found.")


def game_starting():
    # First things first
    gu.wait_game_to_load()
    gu.wait_update()
    gu.close_main_menu_popup()


def game_daily():
    # Campaign tab
    gl.collect_loot()
    gl.battle()
    gl.fast_rewards()
    gl.collect_loot()

    # Dark Forest
    gl.kings_tower()
    gl.arena_of_heroes()
    gl.bounty_board()

    # Ranhorn
    gl.guild()
    gl.the_oak_inn()
    gl.temple_of_ascension()
    gl.resonating_crystal()
    gl.the_noble_tavern()
    gl.store()
    # End
    gl.quests()
    gl.marchants()
    gl.mail()


check_config()
check_adb()

adb.dev()

if False:
    game_starting()
    game_daily()

