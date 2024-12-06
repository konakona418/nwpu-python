from pydantic import BaseModel, Field


class OaLoginMfaData(BaseModel):
    mfa_type_secure_phone: bool = Field(alias="mfaTypeSecurePhone")
    mfa_type_qr_code: bool = Field(alias="mfaTypeQrCode")
    need: bool
    mfa_type_app_push: bool = Field(alias="mfaTypeAppPush")
    mfa_type_face_verify: bool = Field(alias="mfaTypeFaceVerify")
    mfa_enabled: bool = Field(alias="mfaEnabled")
    state: str
    mfa_type_secure_email: bool = Field(alias="mfaTypeSecureEmail")

    class Config:
        populate_by_name = True

class OaLoginMfaResponse(BaseModel):
    code: int
    data: OaLoginMfaData

    class Config:
        populate_by_name = True