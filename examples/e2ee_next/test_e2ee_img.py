# -*- coding: utf-8 -*-
from CHRLINE import *
from CHRLINE.hooks import HooksTracer
import time
import base64
import json

cl = CHRLINE(device="DESKTOPWIN", useThrift=True, debug=False)

tracer = HooksTracer(
    cl, prefixes=["!", ".", "?", "/"], db_type=2
)


class EventHook:
    @tracer.Event
    def onReady():
        print("Ready!")


class OpHook(object):
    @tracer.Operation(25)
    def sendMessage(self, op, cl):
        msg = op.message
        self.trace(msg, self.HooksType["Content"], cl)

    @tracer.Operation(26)
    def recvMessage(self, op, cl):
        msg = op.message
        self.trace(msg, self.HooksType["Content"], cl)


class ContentHook(object):
    @tracer.Content(0)
    def TextMessage(self, msg, cl):
        hooked = self.trace(msg, self.HooksType["Command"], cl)

    @tracer.Content(1)
    def ImageMessage(self, msg, cl):
        id = msg.id
        metadata = msg.contentMetadata
        if msg.chunks:
            keyMaterial = cl.decryptE2EEMessage(msg, msg.opType == 25)["keyMaterial"]

            def genMeta(msgid):
                t = str(msgid)
                r = [11, 0, 4]
                r += cl.getStringBytes(t)
                r += [15, 0, 27, 12, 0, 0, 0, 0, 0]
                r = base64.b64encode(bytes(r)).decode()
                return base64.b64encode(json.dumps({"message": r}).encode()).decode()

            enc_data = cl.downloadObjectForService(
                metadata["OID"],
                None,
                "talk/" + metadata["SID"],
                additionalHeaders={"X-Talk-Meta": genMeta(msg.id)},
            )
            dec_data = cl.decryptByKeyMaterial(enc_data, keyMaterial)
            with open(r"./temp_dec_img.jpg", "wb") as f:
                f.write(dec_data)


class NormalCmd(object):
    @tracer.Command(alt=["sp"], ignoreCase=True, toType=[0])
    def upimg(self, msg, cl):
        """test img"""
        file_path = r"./chrline_logo.png"
        cl.uploadMediaByE2EE(file_path, "image", msg.to)


tracer.run()
