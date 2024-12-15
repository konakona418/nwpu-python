from aiohttp import ClientSession

from edu.edu_oa import EduOaRequest
from edu.edu_struct import EduNotificationResponse
from utils.common import DEFAULT_HEADER

class EduUrls:
    NOTIFICATION = "https://jwxt.nwpu.edu.cn/student/my-notification/get-notifications"


class EduRequest:
    headers: dict = DEFAULT_HEADER.copy()
    def __init__(self, sess: ClientSession, force_auth: bool = False):
        self.sess = sess

        if force_auth:
            EduOaRequest.authorize(sess)

    async def get_notification(self) -> EduNotificationResponse:
        resp = await self.sess.get(EduUrls.NOTIFICATION, headers=self.headers)
        return EduNotificationResponse(**await resp.json())
