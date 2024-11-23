from openai import OpenAI

class ChatSession:
    def __init__(self, max_turns=20):
        self._history = []
        self._max_turns = max_turns

    def add_history(self, role, message):
        if self._history and self._history[-1].get("role") == role:
            # same role, append text
            self._history[-1]["content"] =  self._history[-1].get("content", '') + ' ' + message
        else:
            self._history.append({ "role": role, "content": message })
            if len(self._history) > self._max_turns:
                self._history = self._history[-self._max_turns:]

    def reset(self):
        self._history = []

    def ingest_notify(self, rcr):
        print(f"Notify session")
        # RULES - speech field is what 'assistant' said, but we should skip the [animation]
        # 'user' speech comes from extra_lines[].text when .context_type=='input'
        for line in rcr.get('extra_lines', []):
            if line['context_type'] == 'input':
                self.add_history('user', line['text'])
        speech = rcr.get('speech')
        if speech and 'animation:' not in speech:
            self.add_history('assistant', speech)

    def next_response(self, speech):
        print(f'Inference using history:\n{self._history}')
        return f"chat history {len(self._history)}"


class SingleContextChatSession(ChatSession):
    def __init__(self, max_turns=20):
        super().__init__(max_turns)        
        self._context = [ { "role": "system", 
            "content": "You are a having a conversation with your friend. Make it interesting and keep the conversation moving forward. Your utterances are around 30-40 words long. Ask only one question per response and ask it at the end of your response."
            } ]
    def next_response(self, speech):
        print(f'Open AI Inference using history:\n{self._history}')
        thisinput = [ { "role": "user", "content": speech } ]
        client = OpenAI()
        return client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self._context + self._history + thisinput,
                    max_tokens=70,
                    temperature=0.5
                ).choices[0].message.content


class RemoteChat:
    def __init__(self, server):
        self._server = server
        self._device_sessions = {}
        self._modules = { }
        self.register_module('OPENMOXIE_CHAT', 'default', SingleContextChatSession)

    def register_module(self, module_id, content_id, cname):
        self._modules[f'{module_id}/{content_id}'] = cname

    def get_session(self, device_id, id, cname):
        # each device has a single session only for now
        if device_id in self._device_sessions:
            if self._device_sessions[device_id]['id'] == id:
                return self._device_sessions[device_id]['session']
        print("New session")
        # new session needed
        new_session = { 'id': id, 'session': cname() }
        self._device_sessions[device_id] = new_session
        return new_session['session']

                
    def handle_request(self, device_id, rcr):
        id = rcr.get('module_id', '') + '/' + rcr.get('content_id', '')
        maker = self._modules.get(id)
        if maker:
            print(f'Handling RCR for OPENMOXIE') 
            sess = self.get_session(device_id, id, maker)
            cmd = rcr.get('command')
            if cmd == 'notify':
                sess.ingest_notify(rcr)
            elif cmd == "prompt":
                sess.reset()
                resp = { 'command': 'remote_chat', 'result': 0, 'event_id': rcr['event_id'], 'output': { 'markup': 'Hi there!  Welcome to Open Moxie!'} }
                self._server.send_command_to_bot_json(device_id, 'remote_chat', resp)
            else:
                resp = { 'command': 'remote_chat', 'result': 0, 'event_id': rcr['event_id'], 'output': { 'markup': sess.next_response(rcr["speech"])} }
                self._server.send_command_to_bot_json(device_id, 'remote_chat', resp)
        elif device_id in self._device_sessions:
            del self._device_sessions[device_id]
            print(f'Ignoring request for other module: {rcr.get("module_id")} (Cleared session)')
        else:
            print(f'Ignoring request for other module: {rcr.get("module_id")}')

