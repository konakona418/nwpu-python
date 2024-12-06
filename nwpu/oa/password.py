from typing import Optional

from pydantic import BaseModel, Field


class LoginMfaFormRequest(BaseModel):
    """
    POST
    https://uis.nwpu.edu.cn/cas/mfa/detect
    """
    username: str
    password: str = Field(alias='password')

    class Config:
        populate_by_name = True


class PasswordLoginFormRequest(BaseModel):
    """
    """
    username: str
    password: str = Field(alias='password')
    current_menu: int = Field(alias='currentMenu', default=1)
    mfa_state: str = Field(alias='mfaState')
    geo_location: Optional[str] = Field(alias='geolocation', default='')
    fingerprint: str = Field(alias='fpVisitorId')
    event_id: str = Field(alias='_eventId', default='submit')
    execution: str = Field(alias='execution', default='')

    class Config:
        populate_by_name = True