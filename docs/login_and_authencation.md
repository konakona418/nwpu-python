# 登录与鉴权系统使用方法

>
> **Created on:** 12/10/2024
> 
> **Last Modified on:** 12/10/2024
> 
> **Description:** This document describes the login and authentication 
> mechanism of the NWPU e-campus system.
> 

## 关于登录

准备登陆时，先准备一个 `aiohttp.ClientSession` 对象，利用此对象创建一个 `OaRequest` 对象的实例。

```python
from aiohttp import ClientSession
from nwpu.oa.oa_request import OaRequest

sess = ClientSession(proxy=None)
oa = OaRequest(sess)
```

然后，调用

```python
redirect = 'https://xxx.nwpu.edu.cn/xxx/xxx'
await oa.begin_login(redirect)
```

初始化登录流程。

其中的 `redirect` 参数，表示登录后跳转的页面。此参数为可选的，而且一般说来每个组件都提供了用来手动执行认证的函数，

但是在实际使用中，仍然建议提供一个默认的跳转页面（例如翱翔门户），否则可能导致系统反复要求进行二重认证。

目前提供了三种登录方式：

- 账号密码登录
- 扫码登录
- 短信验证登录

以下分别进行介绍。

### 账号密码登录

要使用账号密码登录，请先获取 RSA 公钥。

```python
rsa_pub_key = await oa.get_rsa_public_key()
```

然后，调用

```python
password = CheckMfaRequiredRequest(username='your_username', 
                                   password=process_password('your_password', rsa))
mfa_resp = await oa.password_init(password)
mfa_required = mfa_resp.data.mfa_required
```

首先，使用用户账密创建了一个 `CheckMfaRequiredRequest` 对象。

然后调用 `password_init` 方法，传入一个 `CheckMfaRequiredRequest` 对象，得到一个 `CheckMfaRequiredResponse` 对象。

使用此对象，我们可以获取 `mfa_required` 字段，如果为 `True`，则需要使用二重身份验证登录；反之，直接登录即可。

**如果需要二重身份验证**，可以按照如下步骤操作（以短信验证为例）：

提取出 `CheckMfaRequiredResponse` 对象中的 `data.state` 字段，

调用 `begin_mfa` 方法，传入 `MfaVerifyMethod.sms` 和 `state`，得到一个 `BeginMfaResponse` 对象。

然后调用 `mfa_send_sms` 方法，传入 `BeginMfaResponse` 对象，发送短信。

接下来，调用 `mfa_verify_sms` 方法，传入 `BeginMfaResponse` 对象和短信验证码，得到一个 `MfaVerifyResponse` 对象。利用此对象，判断短信验证是否成功。

```python
    if mfa_required:
    sms_req = await oa.begin_mfa(MfaVerifyMethod.sms, mfa_resp.data.state)
    await oa.mfa_send_sms(sms_req)
    mfa_result = await oa.mfa_verify_sms(sms_req, input('verify code:'))
    if mfa_result.code == 0:
        print('sms verify succeeded')
    else:
        print('sms verify failed')
        print(mfa_result.data.status)
```

邮箱验证登录与短信验证登录类似，不再赘述。

**接下来的部分，二重验证登录与常规登录一致。**

```python
    password_login = PasswordLoginFormRequest(username=password.username, password=password.password,
                                              mfa_state=mfa_resp.data.state,
                                              fingerprint=generate_fake_browser_fingerprint()[0])

    login_redirects = await oa.finish_password_login(password_login, redirect)
```

首先，创建一个 `PasswordLoginFormRequest` 对象，

传入用户账密和 `mfa_state` （仍然是 `CheckMfaRequiredResponse` 对象中的 `data.state`）字段。

`fingerprint` 是可选的，这里是一个伪造的浏览器指纹。

最后，调用 `finish_password_login` 方法，传入 `PasswordLoginFormRequest` 对象和 `redirect`，得到一个 `LoginRedirects` 对象。
此处的 `redirect` 应当和之前的登录请求中传入的 `redirect` 一致。

这时候，登录就完成了。 `finish_password_login` 方法的返回值为验证时重定向的历史记录。

### 扫码登录

>
> 此部分未经测试
>

首先，调用

```python
qr_init = await oa.qr_init()
state_key = qr_init.data.state_key
```

开始扫码登录流程。

然后，使用 `qr_get_image` 方法，获取图像的 `bytes` 对象，并保存到本地。

在这时，可以调用 `qr_comet` 检查当前扫码状态。

最后，调用

```python
qr_req = QrLoginFormRequest(qr_state_key=state_key)
await oa.finish_qr_login(qr_req, redirect)
```

完成扫码登录。

### 验证码登录

>
> 此部分未经测试
> 

首先调用

```python
req = SmsLoginSendCodeRequest(username='telephone')
await oa.sms_init(req)
```

这会向用户的手机发送一则短信，并返回一个 `SmsLoginSendCodeResponse` 对象。

用户输入短信验证码，调用

```python
req = SmsLoginFormRequest(username='telephone', password='verify_code')
await oa.finish_sms_login(req, redirect)
```

结束短信登录。

## 关于认证

一般说来，组件都会提供用于进行认证的函数。这些函数接受一个 `ClientSession` 作为参数，并进行一系列操作。

认证完毕后，相关的数据会被保存在会话的 `cookies_jar` 中。但在某一组件中，具体是哪些 cookie 在发挥作用，需要视情况而定。

需要注意的是，传入的会话必须已经进行过登录，否则会失败。

认证一般不会返回会话。返回值与具体组件有关。例如，对于邮箱组件：

```python
sid = await MailOaRequest.authorize(sess)
mail_req = MailRequest(sess)
```

这里，调用了 `MailOaRequest.authorize` 方法，传入一个会话对象，得到一个 `str` 类型的 `sid`。

创建 `MailRequest` 对象时，需要传入已经进行了邮箱组件验证的会话。`sid` 可以显式地作为参数进行初始化，
但是不传入也可以，因为 `MailRequest` 会自动从会话中获取。

而对于翱翔门户组件：

```python
token = await ECampusOaRequest.authorize(sess)
ec_req = ECampusRequest(sess, token)
```

这里，调用了 `ECampusOaRequest.authorize` 方法，传入一个会话对象，得到一个 `str` 类型的 `token`。

创建 `ECampusRequest` 对象时，需要传入已经进行了翱翔门户组件验证的会话，以及 `token`。
与邮箱组件不同的是，`token` 必须传入，这是因为无法从直接会话中获取。

如果不传入，构造函数会抛出异常。