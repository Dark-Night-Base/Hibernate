import base64
import socket
import time
from json import loads
from re import findall, sub

import yaml
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'hibernate',
    'version': '0.0.1',
    'name': 'Hibernate',
    'description': "Hibernate your server when no one's online, and resume it when someone login",
    'author': 'Sciroccogti',
    'link': 'https://github.com/Dark-Night-Base/AutoSleep',
}

waitmin = 10  # wait 10min before shutting server down

server_property = {"Version": "", "Protocol": 0, "MaxPlayers": 0}


@new_thread
def stop_server_later(server: ServerInterface, waitmin: int):
    '''After waitmin, shutdown the server and turn on the FakeServer'''
    time.sleep(waitmin * 60)
    # check if there's someone login in the waiting time
    if (Client().getResultNew())["OnlinePlayers"] == 0:
        server.logger.info("Hibernate!")
        server.stop()
        FakeServer(server)


@new_thread
def query_playernum(server: ServerInterface):
    global waitmin
    time.sleep(1)  # in case of server is not ready yet
    playerCount = Client().getResultNew()["OnlinePlayers"]
    if playerCount == 0:
        stop_server_later(server, waitmin)  # TODO: read waitmin from config


def on_load(server: ServerInterface, old_module):
    global waitmin
    try:
        with open("config/Hibernate.yml") as file:
            confYaml = yaml.load(file, Loader=yaml.CLoader)
            waitmin = confYaml["waitmin"]
    except:
        server.logger.info('fail to read config file, using default value')
        with open("config/Hibernate.yml", 'w') as file:
            config = {"waitmin": waitmin}
            yaml.dump(config, file)
    server.register_help_message(
        "!!hibernate", "Hibernate server at %dmin after no one's online" % waitmin)
    if server.is_server_startup():
        query_playernum(server)


def on_server_startup(server: ServerInterface):
    query_playernum(server)


def on_player_left(server: ServerInterface, player: str):
    query_playernum(server)


def pic2base() -> bytes:
    '''encode the server-icon.png to base64'''
    image_path = "server/server-icon.png"  # TODO: read server.properties
    with open(image_path, "rb") as f:
        image = f.read()
        image_base64 = base64.b64encode(image)
        return image_base64


def genStatus() -> bytes:
    msg = '{"description":{"text":"server is sleeping, connect to wake it!"},\
    "players":{"max":%d,"online":0},\
    "version":{"name":"%s","protocol":%d},\
    "favicon":"data:image/png;base64,' % (server_property["MaxPlayers"], server_property["Version"], server_property["Protocol"])
    # the favicon is https://minecraft-zh.gamepedia.com/File:White_Bed_JE3_BE2.png
    faviconBytes = b'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'
    statusBytes = msg.encode("utf-8") + faviconBytes + '"}'.encode("utf-8")
    statusBytes = bytes(encode_varint(len(statusBytes)),
                        "latin-1") + statusBytes
    statusBytes = b'\x00' + statusBytes
    statusBytes = bytes(encode_varint(len(statusBytes)),
                        "latin-1") + statusBytes
    return statusBytes


# def genLoginReturn() -> bytes:
#     msg = 'Server is starting... Please wait for a minute and try again!!\
#         For more information, check website https://mc.sciroccogti.top/!'
#     ret = msg.encode("utf-8")
#     ret = bytes(encode_varint(len(ret)), "latin-1") + ret
#     return ret

@new_thread
def FakeServer(server: ServerInterface):
    '''
    Act as a server when the Java server is shut down
    ping request1: L1 \x00\xc2\x04 HOST c \xdd\x01\x01\x00
        L1: length from \x00 to \x01 (included)
        e.g. \x16\x00\xc2\x04\x12tis.union.worldc\xdd\x01\x01\x00
    ping request2: \xfe\x01\xfa\x00\x0b MC|PingHost+HOST \x00\x00 c \xdd
        e.g. \xfe\x01\xfa\x00\x0bMC|PingHost+tis.union.world\x00\x00c\xdd
    login request: L1 \x00\xc2\x04 HOST c \xdd\x02\r\x00 L2 USER
        L1: length from \x00 to \x02 (included)
        L2: length of USER
        e.g. \x16\x00\xc2\x04\x12tis.union.worldc\xdd\x02\r\x00\x0bSciroccogti
    '''
    print("FakeServer!")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TODO: read port from server.properties
    while True:  # waiting for port exiting TIME_WAIT
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server_socket.bind((socket.gethostname(), 25565))
        except Exception as err:
            print("port is been using", err)
            server_socket.close()
            time.sleep(1)
        else:
            print("Connected!")
            break

    server_socket.listen(128)
    try:
        while True:
            client_socket, client_addr = server_socket.accept()  # wait for client
            recv_data = client_socket.recv(1024)  # UTF-16
            # print(recv_data)
            # print(recv_data.decode("unicode-escape"))

            dataLength = decode_varint(recv_data[:2].decode("latin-1")) + 2

            # Judge if is "MC|PingHost+`ip`" or ping request 1
            if ((recv_data[0:2] == b"\xfe\x01"  # frame head
                    and recv_data[5:27].decode("utf-16-be") == "MC|PingHost")
                    or len(recv_data) < dataLength + 2):
                server.logger.debug("FakeServer get a ping")
                client_socket.send(genStatus())
                client_socket.close()
            else:  # login request
                # start server here
                server.logger.debug("FakeServer get a login request")
                server.start()
                # client_socket.send(genLoginReturn())
                client_socket.close()
                server_socket.close()

    except:
        server_socket.close()


class Client(object):
    '''https://github.com/Saren-Arterius/MinecraftServerQueryPythonTCP'''

    def __init__(self, host=socket.gethostname(), port=25565, timeout=5):
        self.host = host
        self.port = port  # 0 to use any available port
        self.timeout = timeout

    def __getDataNew(self):
        from struct import pack
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.settimeout(self.timeout)
        s.connect((self.host, self.port))

        handShake = b"\x00"
        handShake += b"\x04"
        handShake += bytes(encode_varint(len(self.host)), "UTF-8")
        handShake += bytes(self.host, "UTF-8")
        handShake += pack("H", self.port)
        handShake += b"\x01"
        handShake = bytes(encode_varint(len(handShake)), "UTF-8") + handShake
        s.sendall(handShake)
        s.sendall(b'\x01\x00')

        data = s.recv(1024)
        dataLength = decode_varint(data[:2].decode("latin-1")) + 2
        while 1:
            recv = s.recv(1024)
            data += recv
            if len(data) == dataLength:
                break
        s.close()
        assert data[2:3] == b"\x00"
        assert decode_varint(data[3:5].decode("latin-1")) == len(data[5:])
        return data[5:].decode("UTF-8")

    def getResultNew(self):
        global server_property
        status = {"Version": "", "MOTD": "",
                  "OnlinePlayers": 0, "MaxPlayers": 0}
        try:
            jsonData = loads(self.__getDataNew())
            status["Version"] = findall(
                "(\d.\d+.\d)", jsonData["version"]["name"])[0]
            status["Protocol"] = jsonData["version"]["protocol"]
            status["MOTD"] = jsonData["description"]
            status["OnlinePlayers"] = int(jsonData["players"]["online"])
            status["MaxPlayers"] = int(jsonData["players"]["max"])
            status["ServerIcon"] = sub("\n", "", jsonData["favicon"])
        except Exception as e:
            print("Error in getResultNew:", e)
        finally:
            server_property["Version"] = status["Version"]
            server_property["MaxPlayers"] = status["MaxPlayers"]
            server_property["Protocol"] = status["Protocol"]
            return status


def encode_varint(value):
    return "".join(encode_varint_stream([value]))


def decode_varint(value):
    return decode_varint_stream(value).__next__()


def encode_varint_stream(values):
    for value in values:
        while True:
            if value > 127:
                yield chr((1 << 7) | (value & 0x7f))
                value >>= 7
            else:
                yield chr(value)
                break


def decode_varint_stream(stream):
    value = 0
    base = 1
    for raw_byte in stream:
        val_byte = ord(raw_byte)
        value += (val_byte & 0x7f) * base
        if (val_byte & 0x80):
            base *= 128
        else:
            yield value
            value = 0
            base = 1
