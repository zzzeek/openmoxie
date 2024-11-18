
class RemoteChat:
    def __init__(self, server):
        self._server = server
        pass

    def handle_request(self, device_id, rcr):
        if rcr.get('module_id') == "OPENMOXIE_CHAT":
            print(f'Handling RCR for OPENMOXIE') 
            cmd = rcr.get('command')
            if cmd == 'notify':
                pass
            elif cmd == "prompt":
                resp = { 'command': 'remote_chat', 'result': 0, 'event_id': rcr['event_id'], 'output': { 'markup': 'Hi there'} }
                self._server.send_command_to_bot_json(device_id, 'remote_chat', resp)
            else:
                resp = { 'command': 'remote_chat', 'result': 0, 'event_id': rcr['event_id'], 'output': { 'markup': 'Chat chat chat'} }
                self._server.send_command_to_bot_json(device_id, 'remote_chat', resp)

        else:
            print(f'Ignoring request for other module: {rcr.get("module_id")}')

