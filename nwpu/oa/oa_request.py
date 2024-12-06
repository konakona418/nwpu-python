import random
from math import floor

from aiohttp import ClientSession
from urllib.parse import quote, urlparse, parse_qs

from nwpu.oa.mfa import OaLoginMfaResponse
from nwpu.oa.password import LoginMfaFormRequest, PasswordLoginFormRequest
from nwpu.oa.qrcode import QrInitResponse, QrLoginFormRequest, QrCometResponse
from nwpu.utils.common import DEFAULT_HEADER, timestamp_mill
from nwpu.utils.crypto import wrap_password, encrypt_password
from nwpu.utils.parse import StringArgsBuilder, find_tracer_id


class OaRequestUrl:
    #OA_BEGIN_AUTHORIZE = 'https://uis.nwpu.edu.cn/cas/oauth2.0/authorize'
    OA_PUBLIC_KEY = 'https://uis.nwpu.edu.cn/cas/jwt/publicKey'
    OA_QR_INIT = 'https://uis.nwpu.edu.cn/cas/qr/init'
    OA_QR_IMAGE = 'https://uis.nwpu.edu.cn/cas/qr/qrcode'
    OA_QR_COMET = 'https://uis.nwpu.edu.cn/cas/qr/comet'
    OA_LOGIN = 'https://uis.nwpu.edu.cn/cas/login'
    OA_PWD_DETECT = 'https://uis.nwpu.edu.cn/cas/mfa/detect'


class OaRequest:
    sess: ClientSession
    tracer_id: str
    def __init__(self, sess: ClientSession):
        self.sess: ClientSession = sess
        self.tracer_id = ''

    def set_cookie(self, cookie: str):
        self.sess.cookie_jar.update_cookies({'SESSION': cookie})

    async def begin_oa_session(self, redirect_url ='') -> str:
        resp = await self.sess.get(
            OaRequestUrl.OA_LOGIN + '?service=' + redirect_url,
            headers=DEFAULT_HEADER,
            allow_redirects=True)
        if len((tracer := find_tracer_id(await resp.text()))) > 0:
            self.tracer_id = tracer[0]
        return self.sess.cookie_jar.filter_cookies(resp.url).get('SESSION').value

    async def get_public_key(self) -> str:
        resp = await self.sess.get(OaRequestUrl.OA_PUBLIC_KEY, headers=DEFAULT_HEADER)
        return await resp.text()

    async def qr_init(self) -> QrInitResponse:
        resp = await self.sess.post(OaRequestUrl.OA_QR_INIT, headers=DEFAULT_HEADER)
        return QrInitResponse(**await resp.json())

    async def qr_get_image(self) -> bytes:
        ts_mill = timestamp_mill() + floor(random.random() * 24)
        resp = await self.sess.get(
            StringArgsBuilder(OaRequestUrl.OA_QR_IMAGE)
                .add_param('r', str(ts_mill))
                .build(),
            headers=DEFAULT_HEADER,
        )
        return await resp.read()

    async def qr_comet(self) -> QrCometResponse:
        resp = await self.sess.post(OaRequestUrl.OA_QR_COMET, headers=DEFAULT_HEADER)
        return QrCometResponse(**await resp.json())

    async def password_init(self, form_data: LoginMfaFormRequest) -> OaLoginMfaResponse:
        data = form_data.model_dump(by_alias=True)
        resp = await self.sess.post(
            OaRequestUrl.OA_PWD_DETECT,
            headers=DEFAULT_HEADER,
            data=data,
        )
        return OaLoginMfaResponse(**await resp.json())

    async def complete_qr_login(self, form_data: QrLoginFormRequest, redirect_url ='') -> list[str]:
        redirects = list()
        if self.tracer_id != '':
            print('tracer_id: ' + self.tracer_id)
            form_data.execution = self.tracer_id
        data = form_data.model_dump(by_alias=True)
        resp = await self.sess.post(
            StringArgsBuilder(OaRequestUrl.OA_LOGIN)
                .add_param('service', redirect_url)
                .build(),
            headers=DEFAULT_HEADER,
            data=data,
            allow_redirects=False
        )
        while resp.status == 302:
            redirect_target = resp.headers.get('Location')
            if redirect_target.endswith('/authorize'):
                args = urlparse(redirects[0]).query
                redirect_target += ('?' + args)
            redirects.append(redirect_target)
            resp = await self.sess.post(redirect_target, headers=DEFAULT_HEADER, allow_redirects=False)
            if resp.status == 405:
                resp = await self.sess.get(redirect_target, headers=DEFAULT_HEADER, allow_redirects=False)
            print(resp.status)

        return redirects

    async def complete_password_login(self, redirect_url: str, form_data: PasswordLoginFormRequest) -> list[str]:
        redirects = list()
        if self.tracer_id != '':
            print('tracer_id: ' + self.tracer_id)
            form_data.execution = self.tracer_id
        data = form_data.model_dump(by_alias=True)

        resp = await self.sess.post(
            OaRequestUrl.OA_LOGIN + '?service=' + redirect_url,
            headers=DEFAULT_HEADER,
            allow_redirects=False,
            data=data)
        while resp.status == 302:
            redirect_target = resp.headers.get('Location')
            # todo: this is a temporary hack!!
            if redirect_target.endswith('/authorize'):
                args = urlparse(redirects[0]).query
                redirect_target += ('?' + args)
            redirects.append(redirect_target)
            resp = await self.sess.post(redirect_target, headers=DEFAULT_HEADER, allow_redirects=False)
            if resp.status == 405:
                resp = await self.sess.get(redirect_target, headers=DEFAULT_HEADER, allow_redirects=False)

        return redirects


