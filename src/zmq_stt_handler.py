from moxie_zmq_handler import ZMQHandler
from protos.embodied.perception.audio.zmqSTT_pb2 import zmqSTTRequest,zmqSTTResponse
import soundfile as sf
import numpy as np
import io

class STTSession:
    def __init__(self, parent, device_id, session_id):
        self._parent = parent
        self._device_id = device_id
        self._session_id = session_id
        self._stream_bytes = bytearray()
    def on_request(self, req):
        self._stream_bytes += req.audio_content
    def perform(self):
        buffer = io.BytesIO()
        sf.write(
            buffer,  # File-like object (None for bytes)
            np.frombuffer(self._stream_bytes, dtype=np.int16),
            16000,
            format='WAV',
            subtype='PCM_16'  # 16-bit PCM
            )
        wav_bytes = buffer.getvalue()
        # This we can send to whisper... or... just log it for now
        logfile = f'{self._session_id}.wav'
        with open(logfile, 'wb') as f:
            f.write(wav_bytes)
            print(f'Wrote WAV data to {logfile}')

class STTHandler(ZMQHandler):

    def __init__(self, server):
        super().__init__(server)
        self._sessions = {}

    def handle_zmq(self, device_id, protoname, protodata):
        req = zmqSTTRequest()
        req.ParseFromString(protodata)
        sesskey = ( device_id, req.uuid )
        if sesskey not in self._sessions:
            self._sessions[sesskey] = STTSession(self, sesskey[0], sesskey[1])
        self._sessions[sesskey].on_request(req)
        if req.vad == req.VADState.END_OF_SPEECH:
            # session is done, do the work
            sess = self._sessions.pop(sesskey)
            # TODO: Background this
            sess.perform()
