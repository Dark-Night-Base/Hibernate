from mcdreforged.api.all import *
import time

PLUGIN_METADATA = {
	'id': 'autosleep',
	'version': '0.0.1',
	'name': 'Auto Sleep',
	'author': 'Sciroccogti',
	'link': 'https://github.com/Dark-Night-Base/AutoSleep',
}

playerCount = 0

# def on_info(server: ServerInterface, info: Info):


@new_thread
def stop_server_later(server: ServerInterface, waitmin: int):
    global playerCount
    time.sleep(waitmin * 60)
    if playerCount == 0:
        server.say("Auto Sleep!")
        server.stop()


def on_load(server: ServerInterface, old_module):
    # server.register_command(Literal('!!autosleep').then(Literal('help').runs()))
    global playerCount
    playerCount = 0
    server.register_help_message(
        "!!autosleep", "Sleep server at 10min after no one's online")


def on_player_joined(server: ServerInterface, player: str, info: Info):
    global playerCount
    playerCount += 1


def on_player_left(server: ServerInterface, player: str):
    global playerCount
    if playerCount > 0:
        playerCount -= 1
        if playerCount == 0:
            server.say("waiting to sleep")
            stop_server_later(server, 1)
