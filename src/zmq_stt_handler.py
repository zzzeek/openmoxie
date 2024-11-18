from moxie_zmq_handler import ZMQHandler

class STTHandler(ZMQHandler):

    def handle_zmq(self, device_id, protoname, protodata):
        print(f'STT Handler RX: {protoname}')

