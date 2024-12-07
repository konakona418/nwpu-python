import json
import random

from aiohttp import ClientSession

from ecampus.ec_oa import ECampusOaRequest
from utils.common import DEFAULT_HEADER
from ecampus.ec_struct import *

class ECampusUrl:
    HAS_NEW_EMAIL = "https://portal-service.nwpu.edu.cn/portalCenter/v2/personalData/getEmailDataNew"
    USER_INFO = "https://authx-service.nwpu.edu.cn/personal/api/v1/personal/me/user"
    USER_PORTRAIT = "https://authx-service.nwpu.edu.cn/personal/api/v1/me/portrait"
    USER_PAPER = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPaper"
    USER_CARD = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyECard"
    USER_NETWORK_FEE = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getNetworkFeeInfo"
    USER_BORROW_BOOKS = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyBooks"
    USER_PROPERTY = "https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPropertyInfo"
    USER_EVENTS = "https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/getEvents"

class ECampusRequest:
    sess: ClientSession
    headers: dict = DEFAULT_HEADER.copy()

    def __init__(self, sess: ClientSession, x_token: str):
        self.sess: ClientSession = sess

        if x_token:
            self.sess.headers['X-Id-Token'] = x_token

    async def get_ecampus_token(self) -> str:
        """
        Get ecampus token.
        Call this method if the x-token is not provided at initialization.
        :param sess:
        :return:
        """
        token = await ECampusOaRequest.get_ecampus_token(self.sess)
        self.sess.headers['X-Token'] = token
        return token
    
    async def get_new_email(self) -> ECampusHasNewEmailResponse:
        """
        Get new email status.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.HAS_NEW_EMAIL, headers=self.headers)
        return ECampusHasNewEmailResponse(**await resp.json())
    
    async def get_user_info(self) -> ECampusUserInfoResponse:
        """
        Get user info.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_INFO, headers=self.headers)
        return ECampusUserInfoResponse(**await resp.json())
    
    async def get_user_portrait(self) -> bytes:
        """
        Get user portrait.
        :return:
        """
        req = ECampusUserPortraitRequest(x_token=self.sess.headers['X-Token'],
            random_number=random.randint(100, 999))
        resp = await self.sess.get(ECampusUrl.USER_PORTRAIT, 
                                   headers=self.headers, 
                                   params=req.model_dump(by_alias=True))
        
        return await resp.read()
    
    async def get_user_papers(self) -> ECampusUserPapersResponse:
        """
        Get user papers.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_PAPER, headers=self.headers)
        return ECampusUserPapersResponse(**await resp.json())
    
    async def get_user_card(self) -> ECampusUserCardResponse:
        """
        Get user card.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_CARD, headers=self.headers)
        return ECampusUserCardResponse(**await resp.json())
    
    async def get_user_network_fee(self) -> ECampusUserNetworkFeeResponse:
        """
        Get user network fee.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_NETWORK_FEE, headers=self.headers)
        return ECampusUserNetworkFeeResponse(**await resp.json())
    
    async def get_user_borrow_books(self) -> ECampusUserBorrowBooksResponse:
        """
        Get user borrow books.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_BORROW_BOOKS, headers=self.headers)
        return ECampusUserBorrowBooksResponse(**await resp.json())
    
    async def get_user_property(self) -> ECampusUserPropertyResponse:
        """
        Get user property.
        needs further testing
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_PROPERTY, headers=self.headers)
        return ECampusUserPropertyResponse(**await resp.json())
    
    async def get_user_events(self, request: ECampusUserEventsRequest) -> ECampusUserEventsResponse:
        """
        Get user events.
        :return:
        """
        resp = await self.sess.get(ECampusUrl.USER_EVENTS,
                                   headers=self.headers,
                                   params=request.model_dump(by_alias=True)) # temporary hack
        return ECampusUserEventsResponse(**await resp.json())
