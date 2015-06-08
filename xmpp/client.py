# -*- coding: utf-8 -*-

from sleekxmpp import ClientXMPP


class XMPPConnection(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.register_plugin('xep_0054')
        self.register_plugin('xep_0084')
        self.register_plugin('xep_0153')

        self.connect()
        self.process(block=False)

    def set_vcard(self, name=None, url=None):
        vcard = self['xep_0054'].stanza.VCardTemp()
        vcard['JABBERID'] = self.boundjid.bare

        if name:
            vcard['FN'] = name
            vcard['NICKNAME'] = name

        if url:
            vcard['URL'] = url

        self['xep_0054'].publish_vcard(vcard)

    def set_avatar(self, avatar_data, mime_type='image/png'):
        if avatar_data:
            avatar_id = self['xep_0084'].generate_id(avatar_data)
            info = {
                'id': avatar_id,
                'type': mime_type,
                'bytes': len(avatar_data)
            }
            self['xep_0084'].publish_avatar(avatar_data)
            self['xep_0084'].publish_avatar_metadata(items=[info])
            self['xep_0153'].set_avatar(avatar=avatar_data, mtype=mime_type)
