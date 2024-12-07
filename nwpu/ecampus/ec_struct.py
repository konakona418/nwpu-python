from enum import Enum
from typing import Optional, List, Dict, Any, Literal

from pydantic import BaseModel, Field
from datetime import date, datetime

from pydantic.main import IncEx


class ECampusHasNewEmailRequest(BaseModel):
    """
    GET
    https://portal-service.nwpu.edu.cn/portalCenter/v2/personalData/getEmailDataNew
    """
    pass

class ECampusHasNewEmailData(BaseModel):
    new_email_amount: Optional[int | str] = Field(alias='newEmailAmount', default=0)
    garbage_email_amount: Optional[int | str] = Field(alias='barbageEmailAmount', default=0)
    mailbox_unread_url: Optional[str] = Field(alias='mailboxUnreadUrl', default='')
    app_url: str = Field(alias='appUrl')
    is_main_email: bool = Field(alias='isMainEmail')
    email: str = Field(alias='email')

    class Config:
        populate_by_name = True

class ECampusHasNewEmailResponse(BaseModel):
    code: int
    message: str | None = Field(default='')
    data: Optional[List[ECampusHasNewEmailData]] | None = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserInfoRequest(BaseModel):
    """
    GET
    https://authx-service.nwpu.edu.cn/personal/api/v1/personal/me/user
    """
    pass

class ECampusUserInfoAttributes(BaseModel):
    organization_id: str = Field(alias="organizationId")
    identity_type_code: str = Field(alias="identityTypeCode")
    account_id: str = Field(alias="accountId")
    organization_name: str = Field(alias="organizationName")
    organization_code: str = Field(alias="organizationCode")
    image_url: str = Field(alias="imageUrl")
    identity_type_name: str = Field(alias="identityTypeName")
    identity_type_id: str = Field(alias="identityTypeId")
    user_name: Optional[str] = Field(alias="userName")
    user_id: str = Field(alias="userId")
    user_uid: str = Field(alias="userUid")

    class Config:
        populate_by_name = True

class ECampusUserInfoData(BaseModel):
    username: str
    roles: List[str]
    attributes: Optional[ECampusUserInfoAttributes] = Field(default=None)

    class Config:
        populate_by_name = True

class ECampusUserInfoResponse(BaseModel):
    acknowledged: Optional[bool] = Field(alias="acknowleged", default=True)
    code: int
    message: Optional[str]
    data: Optional[ECampusUserInfoData] = Field(default=None)

    class Config:
        populate_by_name = True

class ECampusUserPortraitRequest(BaseModel):
    """
    GET
    https://authx-service.nwpu.edu.cn/personal/api/v1/me/portrait
    GET parameters
    """
    x_token: str = Field(alias='token')
    random_number: Optional[int | None] = Field(alias='random_number', default=None)

    class Config:
        populate_by_name = True


class ECampusUserPortraitResponse(BaseModel):
    """
    binary
    """
    pass

class ECampusUserInfoAccurateRequest(BaseModel):
    """
    GET
    https://authx-service.nwpu.edu.cn/personal/api/v1/personal/user/info
    """
    pass

class ECampusUserInfoAccurateResponse(BaseModel):
    # todo
    pass

class ECampusUserPapersRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPaper
    """
    pass

class ECampusUserPapersResponse(BaseModel):
    code: int = Field(alias='code', default=0)
    message: Optional[str] = Field(default='')
    data: Optional[Dict[str, Any]] | None = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ECampusUserCardRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyECard
    """
    
class ECampusUserCardExpenditure(BaseModel):
    time: str
    amount: str
    address: Optional[str] = ""
    pay_way: str = Field(alias="payWay")

    class Config:
        populate_by_name = True


class ECampusUserCardLastCas(BaseModel):
    time: Optional[str] = ""
    address: Optional[str] = ""

    class Config:
        populate_by_name = True


class ECampusUserCardData(BaseModel):
    last_expenditure: List[ECampusUserCardExpenditure | Any] | None = Field(alias="lastExpenditure", default=None)
    last_income: List = Field(alias="lastIncome")
    balance: str
    e_card_type: str = Field(alias="eCardType")
    card_status: str = Field(alias="cardStatus")
    open_date: Optional[str] = Field(alias="openDate", default="")
    month_balance: str = Field(alias="monthBalance")
    app_url: str = Field(alias="appUrl")
    pc_url: Optional[str] = Field(alias="pcUrl", default="")
    last_cas: Optional[ECampusUserCardLastCas] = Field(alias="lastCas", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserCardResponse(BaseModel):
    code: int
    message: Optional[str]
    data: Optional[ECampusUserCardData] = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserNetworkFeeRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getNetworkFeeInfo
    """
    pass


class ECampusUserNetworkFeeFlow(BaseModel):
    flow_month: str = Field(alias="flowMonth")
    flow_sum_bytes: str = Field(alias="flowSumBytes")
    flow_used_bytes: str = Field(alias="flowUsedBytes")

    class Config:
        populate_by_name = True


class ECampusUserNetworkFeeData(BaseModel):
    user_balance: str = Field(alias="userBalance")
    package_name: str = Field(alias="packageName")
    pc_url: str = Field(alias="pcUrl")
    app_url: str = Field(alias="appUrl")
    package_flow: str = Field(alias="packageFlow")
    residue_flow: str = Field(alias="residueFlow")
    account_balance: str = Field(alias="accountBalance")
    residue_balance: str = Field(alias="residueBalance")
    flow_list: List[ECampusUserNetworkFeeFlow | Any] | None = Field(alias="flowList", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserNetworkFeeResponse(BaseModel):
    code: int
    message: Optional[str] = None
    data: Optional[ECampusUserNetworkFeeData] = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserBorrowBooksRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyBooks
    """
    pass


class ECampusUserBorrowBooksShouldRepayBook(BaseModel):
    should_repay_book_name: str = Field(alias="shouldRepayBookName")
    should_repay_book_date: str = Field(alias="shouldRepayBookDate")

    class Config:
        populate_by_name = True


class ECampusUserBorrowBooksData(BaseModel):
    book_id: Optional[str] = Field(None, alias="bookId")
    borrow_count: str = Field(alias="borrowCount")
    book_average: str = Field(alias="bookArrearage")
    book_past_due: str = Field(alias="bookPastDue")
    pc_url: str = Field(alias="pcUrl")
    app_url: str = Field(alias="appUrl")
    should_repay_list: List[ECampusUserBorrowBooksShouldRepayBook] | None = Field(alias="shouldRepayList", default=None)

    class Config:
        populate_by_name = True


class ECampusUserBorrowBooksResponse(BaseModel):
    code: int
    message: Optional[str]
    data: Optional[ECampusUserBorrowBooksData] = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserPropertyRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPropertyInfo
    """
    pass

class ECampusUserPropertyData(BaseModel):
    property_sum: str = Field(alias="propertySum")
    property_sum_unit: str = Field(alias="propertySumUnit")
    property_amount: float = Field(alias="propertyAmount")
    property_amount_unit: str = Field(alias="propertyAmountUnit")
    pc_url: str = Field(alias="pcUrl")
    app_url: str = Field(alias="appUrl")
    property_info_list: List[dict | Any] | None = Field(alias="propertyInfoList", default=None)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserPropertyResponse(BaseModel):
    code: int
    message: Optional[str]
    data: Optional[ECampusUserPropertyData] | None = Field(default=None)
    
    class Config:
        populate_by_name = True

class ECampusUserEventsMode(str, Enum):
    date_view = "DateView"

class ECampusUserEventsRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/getEvents?
    GET params
    """

    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    mode: ECampusUserEventsMode = Field(alias="reqType", default=ECampusUserEventsMode.date_view)
    random_number: str | int | None = Field(alias="randomNumber", default=0)

    def model_dump(
        self,
        *,
        mode: Literal['json', 'python'] | str = 'python',
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal['none', 'warn', 'error'] = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        dumped = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )
        dumped["startDate"] = dumped["startDate"].strftime("%Y-%m-%d")
        dumped["endDate"] = dumped["endDate"].strftime("%Y-%m-%d")
        dumped["reqType"] = ECampusUserEventsMode(dumped["reqType"]).value
        return dumped

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"),
            date: lambda d: d.strftime("%Y-%m-%d"),
        }

        

class ECampusUserEventsCalendarEntry(BaseModel):
    id: str
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    title: str
    is_whole_day: str = Field(alias="isWholeDay")
    start_date: str = Field(alias="startDate")
    start_time: str = Field(alias="startTime")
    end_date: str = Field(alias="endDate")
    end_time: str = Field(alias="endTime")
    repeat_type: Optional[str] = Field(None, alias="repeatType")
    repeat_cycle_type: Optional[str] = Field(None, alias="repeatCycleType")
    repeat_cycle_space: Optional[str] = Field(None, alias="repeatCycleSpace")
    repeat_cycle_exp: Optional[str] = Field(None, alias="repeatCycleExp")
    repeat_end_type: Optional[str] = Field(None, alias="repeatEndType")
    repeat_end_date: Optional[str] = Field(None, alias="repeatEndDate")
    repeat_end_times: Optional[int] = Field(None, alias="repeatEndTimes")
    address: Optional[str]
    remark: Optional[str]
    create_user: Optional[str] = Field(None, alias="createUser")
    update_user: Optional[str] = Field(None, alias="updateUser")
    create_time: Optional[str] = Field(None, alias="createTime")
    update_time: Optional[str] = Field(None, alias="updateTime")
    start_date_str: str = Field(alias="startDateStr")
    end_date_str: str = Field(alias="endDateStr")
    repeat_end_date_str: Optional[str] = Field(None, alias="repeatEndDateStr")
    create_time_str: Optional[str] = Field(None, alias="createTimeStr")
    create_user_name: Optional[str] = Field(None, alias="createUserName")
    create_user_code: Optional[str] = Field(None, alias="createUserCode")
    update_user_code: Optional[str] = Field(None, alias="updateUserCode")
    timezone: str
    color: str
    cu_color: Optional[str] = Field(None, alias="cucolor")
    calendar_name: str = Field(alias="calendarName")
    remind_type: Optional[str] = Field(None, alias="remindType")
    schedule_date: Optional[str] = Field(None, alias="scheduleDate")
    schedule_date_id: Optional[str] = Field(None, alias="scheduleDateId")
    repeat_cycle_count: Optional[int] = Field(None, alias="repeatCycleCount")
    schedule_type: Optional[str] = Field(None, alias="scheduleType")
    terminal_type: Optional[str] = Field(None, alias="terminalType")
    remind_date: Optional[str] = Field(None, alias="remindDate")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserEventsScheduleDate(BaseModel):
    calendar_list: List[ECampusUserEventsCalendarEntry | Any] | None = Field(alias="calendarList", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserEventsData(BaseModel):
    schedule: Dict[str, ECampusUserEventsScheduleDate | Any] | None = Field(default=None)
    req_type: str = Field(alias="reqType")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserEventsResponse(BaseModel):
    code: int
    message: str
    data: Optional[ECampusUserEventsData] = Field(default=None)

    class Config:
        populate_by_name = True
