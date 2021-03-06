import os
import sys
import logging

## ws_client and msg_ntk path 
sys.path.insert(0, os.path.abspath("../ws_client"))
sys.path.insert(0, os.path.abspath("../msg_ntk"))

from ws_client import WebsocketClient
from msg_ntk import Map2DDataPUB
from msg_ntk import Map2DDataSUB

## LOGGING INFO
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level=logging.INFO)

class EdgeComm():
    def __init__(self):
        # varaibles
        self.ws_hostaddress = 'https://heroku-uni-socket.herokuapp.com/'
        self.ws_sio = ""

        # init
        self.ws = WebsocketClient(self.ws_hostaddress,self.ws_msg)

        self.map_2d_data_sub = Map2DDataSUB(self.map_2d_data_pub_cb)
        
    def ws_msg(self,msg):
        LOGGER.info(" ws -> edge_comm got msg: %s", msg)

    def map_2d_data_pub_cb(self,msg):
        LOGGER.info(" msg_ntk -> edge_comm got msg")
        
        # emit
        self.ws_sio.emit('map_data', {'map': "MAP DATA"})

    
    def start_it(self):
        # ws
        self.ws.start_it()

        # get ws_sio
        self.ws_sio = self.ws.get_ws_sio()

        # msg_ntk
        self.map_2d_data_sub.deamon = True
        self.map_2d_data_sub.start()

if __name__ == '__main__':
    app = EdgeComm()
    app.start_it()


