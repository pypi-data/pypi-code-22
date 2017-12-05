#!/usr/bin/env python3
#
# SynchronousMsgServer is a class that contains a TCP server and Websocket server which run asynchronously
# in a background thread, and also allows synchronous code to send and receives messages with it.
#
# based on:
#   https://stackoverflow.com/questions/29324610/python-queue-linking-object-running-asyncio-coroutines-with-main-thread-input
#   https://stackoverflow.com/questions/32054066/python-how-to-run-multiple-coroutines-concurrently-using-asyncio
#   https://websockets.readthedocs.io/en/stable/intro.html
import os
import sys
import asyncio
import websockets
import janus
import queue

class SynchronousMsgServer:
    def __init__(self, msgLib):
        self.msgLib = msgLib
        self.loop = asyncio.get_event_loop()
        from threading import Thread
        t = Thread(target=self.start)
        t.start()

    def send_message(self, msg):
        self.synchronous_tx_queue.sync_q.put(msg.rawBuffer().raw)
    
    def get_message(self, timeout, msgIds=[]):
        while True:
            try:
                data = self.synchronous_rx_queue.get(True, timeout)
                hdr = self.msgLib.hdr(data)
                id = hdr.GetMessageID()
                if len(msgIds) == 0 or id in msgIds:
                    msg = self.msgLib.MsgFactory(hdr)
                    return msg
            except queue.Empty:
                return None
    
    def stop(self):
        for task in asyncio.Task.all_tasks():
            task.cancel()
        #self.stop()
        self.tcp_server.close()
        self.loop.stop()
        # Some thread hangs and sys.exit doesn't return, perhaps?
        sys.exit(0)

    # Implementation details from here down
    def start(self):
        # general asyncio stuff
        asyncio.set_event_loop(self.loop)
        self.loop = asyncio.get_event_loop()

        # synchronous input/output
        self.synchronous_tx_queue = janus.Queue(loop=self.loop)
        self.synchronous_rx_queue = queue.Queue()
        asyncio.ensure_future(self.handle_synchronous_input())

        # client lists
        self.tcp_clients = {} # task -> (reader, writer)
        self.ws_clients = {}

        # tcp server
        self.tcp_server = self.loop.run_until_complete(asyncio.start_server(self.client_connected_handler, '127.0.0.1', 5678))
        
        # websocket server
        start_ws_server = websockets.serve(self.handle_ws_client, '127.0.0.1', 5679)
        self.loop.run_until_complete(start_ws_server)
        
        # kick things off
        self.loop.run_forever()
        self.stopped()

    async def handle_synchronous_input(self):
        while True:
            data = await self.synchronous_tx_queue.async_q.get()
            await self.send_to_others(self.synchronous_tx_queue, data)

    def stopped(self):
        self.tcp_server.close()
        self.loop.stop()
        self.loop.close()
    
    async def send_to_others(self, me, data):
        if me != self.synchronous_tx_queue:
            try:
                #print("writing to synchronous_rx_queue")
                self.synchronous_rx_queue.put(data)
            except:
                pass

        # send to Websocket clients
        for ws in self.ws_clients.keys():
            if ws != me:
                # calling ws.send REQUIRES an 'await', otherwise data never gets to the ws client!
                await ws.send(data)

        # send to TCP clients
        for task in self.tcp_clients.keys():
                (reader, writer) = self.tcp_clients[task]
                if reader != me:
                    writer.write(data)

    async def handle_tcp_client(self, client_reader):
        #print("handle_tcp_client")
        while True:
            # we *should* read self.msgLib.hdr.SIZE bytes,
            # then parse header to see body length,
            # then read those bytes.
            data = await client_reader.read(1024)
            if not data:
                break
            await self.send_to_others(client_reader, data)

    def client_connected_handler(self, client_reader, client_writer):
        # Start a new asyncio.Task to handle this specific client connection
        task = asyncio.Task(self.handle_tcp_client(client_reader))
        print("Added new client to list of " + str(len(self.tcp_clients)) + " clients")
        self.tcp_clients[task] = (client_reader, client_writer)

        def client_done(task):
            print("client exited")
            # When the tasks that handles the specific client connection is done
            del self.tcp_clients[task]

        # Add the client_done callback to be run when the future becomes done
        task.add_done_callback(client_done)

    async def handle_ws_client(self, websocket, path):
        self.ws_clients[websocket] = websocket
        print("websocket connected")
        try:
            while True:
                data = await websocket.recv()
                if not data:
                    break
                await self.send_to_others(websocket, data)
        except websockets.exceptions.ConnectionClosed:
            print("websocket closed")
            del self.ws_clients[websocket]
