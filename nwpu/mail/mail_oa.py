from pydantic import BaseModel, Field
from aiohttp import ClientSession, ClientResponse
from urllib.parse import unquote, quote

from nwpu.utils.common import DEFAULT_HEADER


class MailOaUrl:
    MAIL_OA_LOCAL = 'https://mail.nwpu.edu.cn/cmcuapi/sso/oauth2'
    MAIL_OA_REDIRECTED_OA = 'https://uis.nwpu.edu.cn/cas/oauth2.0/authorize'


class MailOa2Request(BaseModel):
    """
    GET, has redirect
    https://mail.nwpu.edu.cn/cmcuapi/sso/oauth2
    """
    pass


class MailRedirectedOa2Request(BaseModel):
    """
    GET, has redirect
    """
    pass

class MailOaRequest:
    sess: ClientSession

    def __init__(self, sess: ClientSession):
        self.sess: ClientSession = sess

    async def get_oa_url(self) -> str:
        """
        GET, has redirect
        :return redirected url, should be applied later in oa login.
        """
        async with (self.sess.get(MailOaUrl.MAIL_OA_LOCAL, allow_redirects=False, headers=DEFAULT_HEADER) as resp):
            if resp.status == 302:
                redirect_once = resp.headers['Location']
                async with self.sess.get(redirect_once, allow_redirects=False, headers=DEFAULT_HEADER) as resp:
                    return resp.headers['Location'].split('?', 1)[1].removeprefix('service=')
            return ''

    async def get_oa_session(self) -> str:
        """
        :return:
        """
        async with self.sess.get(MailOaUrl.MAIL_OA_REDIRECTED_OA, allow_redirects=True, headers=DEFAULT_HEADER) as resp:
            cookie = resp.cookies.get('SESSION')
            return cookie.value

def extract_sid(sess: ClientSession) -> str:
    return sess.cookie_jar.filter_cookies('https://mail.nwpu.edu.cn').get('Coremail.sid').value
        