# -*- coding: utf-8 -*-
import base64
import binascii

import httpx
import requests
import rsa

from .exceptions import LineServiceException
from .server import Server
from .services.AccessTokenRefreshService import AccessTokenRefreshService
from .services.AccountAuthFactorEapConnectService import (
    AccountAuthFactorEapConnectService,
)
from .services.AuthService import AuthService
from .services.BuddyService import BuddyService
from .services.CallService import CallService
from .services.ChannelService import ChannelService
from .services.ChatAppService import ChatAppService
from .services.CoinService import CoinService
from .services.E2EEKeyBackupService import E2EEKeyBackupService
from .services.HomeSafetyCheckService import HomeSafetyCheckService
from .services.InterlockService import InterlockService
from .services.LiffService import LiffService
from .services.LoginService import LoginService
from .services.MultiProfileService import MultiProfileService
from .services.PremiumFontService import PremiumFontService
from .services.PremiumStatusService import PremiumStatusService
from .services.PrimaryAccountInitService import PrimaryAccountInitService
from .services.PrimaryAccountSmartSwitchRestorePreparationService import (
    PrimaryAccountSmartSwitchRestorePreparationService,
)
from .services.PrimaryQrCodeMigrationLongPollingService import (
    PrimaryQrCodeMigrationLongPollingService,
)
from .services.PrimaryQrCodeMigrationPreparationService import (
    PrimaryQrCodeMigrationPreparationService,
)
from .services.PrimarySeamlessLoginService import PrimarySeamlessLoginService
from .services.RelationService import RelationService
from .services.SecondaryPwlessLoginPermitNoticeService import (
    SecondaryPwlessLoginPermitNoticeService,
)
from .services.SecondaryPwlessLoginService import SecondaryPwlessLoginService
from .services.SecondarySeamlessLoginService import SecondarySeamlessLoginService
from .services.SettingsService import SettingsService
from .services.ShopCollectionService import ShopCollectionService
from .services.ShopService import ShopService
from .services.SquareBotService import SquareBotService
from .services.SquareLiveTalkService import SquareLiveTalkService
from .services.SquareService import SquareService
from .services.TalkService import TalkService
from .services.TestService import TestService


class API(
    TalkService,
    ShopService,
    LiffService,
    ChannelService,
    SquareService,
    BuddyService,
    PrimaryAccountInitService,
    AuthService,
    SettingsService,
    AccessTokenRefreshService,
    CallService,
    SecondaryPwlessLoginService,
    SecondaryPwlessLoginPermitNoticeService,
    ChatAppService,
    AccountAuthFactorEapConnectService,
    E2EEKeyBackupService,
    SquareBotService,
    TestService,
    HomeSafetyCheckService,
    PrimaryQrCodeMigrationLongPollingService,
    PrimaryQrCodeMigrationPreparationService,
    LoginService,
    InterlockService,
    RelationService,
    SquareLiveTalkService,
    CoinService,
    ShopCollectionService,
    PremiumFontService,
    MultiProfileService,
):
    _msgSeq = 0
    url = "https://gf.line.naver.jp/enc"

    def __init__(self, forwardedIp=None):
        self.server = Server()
        self.req = requests.session()
        self.req_h2 = httpx.Client(http2=True)
        self.server.Headers = {
            "x-line-application": self.APP_NAME,
            "x-le": self.le,
            "x-lap": "5",
            "x-lpv": "1",
            "x-lcs": self._encryptKey,
            "User-Agent": self.LineUserAgent,
            "content-type": "application/x-thrift; protocol=TBINARY",
            "x-lal": self.LINE_LANGUAGE,
            "x-lhm": "POST",
            "X-Line-Chrome-Version": "3.6.0",
        }
        self.log(f"Use User-Agent: {self.USER_AGENT}")
        if forwardedIp is not None:
            self.server.Headers["X-Forwarded-For"] = forwardedIp
        self.authToken = None
        self.revision = 0
        self.globalRev = 0
        self.individualRev = 0
        self._msgSeq = 0
        TalkService.__init__(self)
        ShopService.__init__(self)
        LiffService.__init__(self)
        ChannelService.__init__(self)
        SquareService.__init__(self)
        BuddyService.__init__(self)
        PrimaryAccountInitService.__init__(self)
        AuthService.__init__(self)
        SettingsService.__init__(self)
        AccessTokenRefreshService.__init__(self)
        CallService.__init__(self)
        SecondaryPwlessLoginService.__init__(self)
        SecondaryPwlessLoginPermitNoticeService.__init__(self)
        ChatAppService.__init__(self)
        AccountAuthFactorEapConnectService.__init__(self)
        E2EEKeyBackupService.__init__(self)
        SquareBotService.__init__(self)
        TestService.__init__(self)
        HomeSafetyCheckService.__init__(self)
        PrimaryQrCodeMigrationLongPollingService.__init__(self)
        PrimaryQrCodeMigrationPreparationService.__init__(self)
        LoginService.__init__(self)
        InterlockService.__init__(self)
        RelationService.__init__(self)
        SquareLiveTalkService.__init__(self)
        CoinService.__init__(self)
        ShopCollectionService.__init__(self)
        PremiumFontService.__init__(self)
        self.s_smart_switch = PrimaryAccountSmartSwitchRestorePreparationService(self)
        self.s_multi_profile = MultiProfileService(self.client)
        self.s_premium_status = PremiumStatusService(self.client)
        self.s_seamless = PrimarySeamlessLoginService(self.client)
        self.s_seamless_sec = SecondarySeamlessLoginService(self.client)

    def requestPwlessLogin(self, phone, pw):
        pwless_code = self.checkAndGetValue(self.createPwlessSession(phone), 1, "val_1")
        print(f"PWLESS SESSION: {pwless_code}")
        cert = self.getCacheData(".pwless", phone)
        try:
            self.verifyLoginCertificate(pwless_code, "" if cert is None else cert)
        except:
            pwless_pincode = self.checkAndGetValue(
                self.requestPinCodeVerif(pwless_code), 1, "val_1"
            )
            print(f"PWLESS PINCODE: {pwless_pincode}")
            self.checkPwlessPinCodeVerified(pwless_code)
        secret, secretPK = self.createSqrSecret(True)
        self.putExchangeKey(pwless_code, secretPK)
        self.requestPaakAuth(pwless_code)
        print("need Paak Auth Confind")
        self.checkPaakAuthenticated(pwless_code)
        ek = self.getE2eeKey(pwless_code)
        try:
            loginInfo = self.pwlessLoginV2(pwless_code)
            cert = self.checkAndGetValue(loginInfo, 2, "val_2")
            tokenInfo = self.checkAndGetValue(loginInfo, 3, "val_3")
            token = self.checkAndGetValue(tokenInfo, 1, "val_1")
            token2 = self.checkAndGetValue(tokenInfo, 2, "val_2")
            mid = self.checkAndGetValue(loginInfo, 5, "val_5")
        except:
            loginInfo = self.pwlessLogin(pwless_code)
            token = self.checkAndGetValue(loginInfo, 1, "val_1")
            cert = self.checkAndGetValue(loginInfo, 2, "val_2")
            mid = self.checkAndGetValue(loginInfo, 4, "val_4")
        self.authToken = token
        print(f"Auth Token: {self.authToken}")
        self.saveCacheData(".pwless", phone, cert)
        self.decodeE2EEKeyV1(self.checkAndGetValue(ek, 1, "val_1"), secret, mid)
        return True

    def requestEmailLogin(self, email, pw, e2ee=True):
        rsaKey = self.getRSAKeyInfo()
        keynm = self.checkAndGetValue(rsaKey, 1, "val_1")
        nvalue = self.checkAndGetValue(rsaKey, 2, "val_2")
        evalue = self.checkAndGetValue(rsaKey, 3, "val_3")
        sessionKey = self.checkAndGetValue(rsaKey, 4, "val_4")
        certificate = self.getEmailCert(email)
        message = (
            chr(len(sessionKey))
            + sessionKey
            + chr(len(email))
            + email
            + chr(len(pw))
            + pw
        ).encode("utf-8")
        pub_key = rsa.PublicKey(int(nvalue, 16), int(evalue, 16))
        crypto = binascii.hexlify(rsa.encrypt(message, pub_key)).decode()
        secret, secretPK = self.createSqrSecret(True)
        pincode = b"202202"
        _secret = self._encryptAESECB(
            self.getSHA256Sum(pincode), base64.b64decode(secretPK)
        )
        _req = {
            "keynm": keynm,
            "encData": crypto,
            "secret": _secret,
            "deviceName": self.SYSTEM_MODEL,
            "calledName": "loginZ",
        }
        if not e2ee:
            _req["secret"] = None
        try:
            res = self.loginV2(**_req, cert=certificate)
        except LineServiceException as e:
            res = {}
            if e.code == 89:
                if not e2ee:
                    raise e
                return self.requestEmailLogin(email, pw, False)
            raise e
        if self.checkAndGetValue(res, 1, "val_1") is None:
            verifier = self.checkAndGetValue(res, 3, "val_3")
            if not e2ee:
                pincode = self.checkAndGetValue(res, 4).encode()
            print(f"Enter Pincode: {pincode.decode()}")
            if e2ee:
                e2eeInfo = self.checkLoginV2PinCode(verifier)["metadata"]
                try:
                    self.decodeE2EEKeyV1(e2eeInfo, secret)
                except:
                    raise Exception("e2eeInfo decode failed, try again")
                blablabao = self.encryptDeviceSecret(
                    base64.b64decode(e2eeInfo["publicKey"]),
                    secret,
                    base64.b64decode(e2eeInfo["encryptedKeyChain"]),
                )
                e2eeLogin = self.confirmE2EELogin(verifier, blablabao)
            else:
                e2eeLogin = self.checkLoginZPinCode(verifier)["verifier"]
            try:
                res = self.loginV2(**_req, verifier=e2eeLogin)
                self.saveEmailCert(email, self.checkAndGetValue(res, 2, "val_2"))
            except:
                raise Exception("confirmE2EELogin failed, try again")
        self.authToken = self.checkAndGetValue(res, 1)
        print(f"AuthToken: {self.authToken}")
        return True

    def requestEmailLoginV2(self, email, pw):
        rsaKey = self.getRSAKeyInfo()
        keynm = self.checkAndGetValue(rsaKey, 1, "val_1")
        nvalue = self.checkAndGetValue(rsaKey, 2, "val_2")
        evalue = self.checkAndGetValue(rsaKey, 3, "val_3")
        sessionKey = self.checkAndGetValue(rsaKey, 4, "val_4")
        certificate = self.getEmailCert(email)
        message = (
            chr(len(sessionKey))
            + sessionKey
            + chr(len(email))
            + email
            + chr(len(pw))
            + pw
        ).encode("utf-8")
        pub_key = rsa.PublicKey(int(nvalue, 16), int(evalue, 16))
        crypto = binascii.hexlify(rsa.encrypt(message, pub_key)).decode()
        secret, secretPK = self.createSqrSecret(True)
        pincode = b"1314520"
        _secret = self._encryptAESECB(
            self.getSHA256Sum(pincode), base64.b64decode(secretPK)
        )
        try:
            res = self.loginV2(
                keynm, crypto, _secret, deviceName=self.SYSTEM_MODEL, cert=certificate
            )
        except LineServiceException as e:
            if e.code == 89:
                print(f"can't login: {e.message}, try use LoginZ...")
                return self.requestEmailLogin(email, pw)
            raise e
        if self.checkAndGetValue(res, 9, "val_9") is None:
            verifier = self.checkAndGetValue(res, 3, "val_3")
            if self.checkAndGetValue(res, 5, "val_5") == 3:
                print("need device confirm")
            print(f"Enter Pincode: {pincode.decode()}")
            e2eeInfo = self.checkLoginV2PinCode(verifier)["metadata"]
            try:
                e2eeKeyInfo = self.decodeE2EEKeyV1(e2eeInfo, secret)
            except:
                raise Exception("e2eeInfo decode failed, try again")
            blablabao = self.encryptDeviceSecret(
                base64.b64decode(e2eeInfo["publicKey"]),
                secret,
                base64.b64decode(e2eeInfo["encryptedKeyChain"]),
            )
            e2eeLogin = self.confirmE2EELogin(verifier, blablabao)
            try:
                res = self.loginV2(
                    None, None, None, deviceName=self.SYSTEM_NAME, verifier=e2eeLogin
                )
            except LineServiceException as e:
                print(e)
                if e.code in [20, 89]:
                    print(f"can't login: {e.message}, try use LoginZ...")
                    return self.requestEmailLogin(email, pw)
            self.saveEmailCert(email, self.checkAndGetValue(res, 2, "val_2"))
        loginInfo = self.checkAndGetValue(res, 9, "val_9")
        self.authToken = self.checkAndGetValue(loginInfo, 1, "val_1")
        refreshToken = self.checkAndGetValue(loginInfo, 2, "val_2")
        self.saveCacheData(".refreshToken", self.authToken, refreshToken)
        print(f"AuthToken: {self.authToken}")
        print(f"RefreshToken: {refreshToken}")
        return True

    def requestSQR(self, isSelf=True):
        sqr = self.checkAndGetValue(self.createSession(), 1, "val_1")
        url = self.checkAndGetValue(self.createQrCode(sqr), 1, "val_1")
        secret, secretUrl = self.createSqrSecret()
        url = url + secretUrl
        imgPath = self.genQrcodeImageAndPrint(url)
        yield f"URL: {url}"
        yield f"IMG: {imgPath}"
        if self.checkQrCodeVerified(sqr):
            try:
                self.verifyCertificate(sqr, self.getSqrCert())
            except:
                c = self.checkAndGetValue(self.createPinCode(sqr), 1, "val_1")
                yield f"請輸入pincode: {c}"
                self.checkPinCodeVerified(sqr)
            e = self.qrCodeLogin(sqr, secret)
            if isSelf:
                self.authToken = e
                print(f"AuthToken: {self.authToken}")
            else:
                yield e
            return
            raise Exception("can not check pin code, try again?")
        raise Exception("can not check qr code, try again?")

    def requestSQR2(self, isSelf=True):
        sqr = self.checkAndGetValue(self.createSession(), 1, "val_1")
        url = self.checkAndGetValue(self.createQrCode(sqr), 1, "val_1")
        secret, secretUrl = self.createSqrSecret()
        url = url + secretUrl
        imgPath = self.genQrcodeImageAndPrint(url)
        yield f"URL: {url}"
        yield f"IMG: {imgPath}"
        if self.checkQrCodeVerified(sqr):
            try:
                self.verifyCertificate(sqr, self.getSqrCert())
            except:
                c = self.createPinCode(sqr)
                yield f"請輸入pincode: {c}"
                self.checkPinCodeVerified(sqr)
            try:
                e = self.qrCodeLoginV2(sqr, self.MODEL_NAME, self.USERDOMAIN, False)
                cert = self.checkAndGetValue(e, 1)
                self.saveSqrCert(cert)
                tokenV3Info = self.checkAndGetValue(e, 3)
                _mid = self.checkAndGetValue(e, 4)
                bT = self.checkAndGetValue(e, 9)
                metadata = self.checkAndGetValue(e, 10)
                e2eeKeyInfo = self.decodeE2EEKeyV1(metadata, secret)
                authToken = self.checkAndGetValue(tokenV3Info, 1)
                refreshToken = self.checkAndGetValue(tokenV3Info, 2)
                self.saveCacheData(".refreshToken", authToken, refreshToken)
                print(f"AuthToken: {authToken}")
                print(f"RefreshToken: {refreshToken}")
                if isSelf:
                    self.authToken = authToken
                yield authToken
            except LineServiceException as e:
                if e.code == 100:
                    # BANNED.
                    raise e
                print(e)
                yield "try using requestSQR()..."
                for _ in self.requestSQR(isSelf):
                    yield _
            return
            raise Exception("can not check pin code, try again?")
        raise Exception("can not check qr code, try again?")

    def requestSQR3(self, isSelf=True):
        """
        Request Secondary QrCode Login for secure.

        Source: https://github.com/DeachSword/CHRLINE/blob/445e433b1fbe9a020f6bc1cbd0eb7af3f75ce196/examples/test_sqr_4_secure.py
        """
        log4Debug = False
        sqr = self.checkAndGetValue(self.createSession(), 1)
        qr4s = self.createQrCodeForSecure(sqr)
        self.log(qr4s, log4Debug)
        url = self.checkAndGetValue(qr4s, "callbackUrl", 1)
        nonce = self.checkAndGetValue(qr4s, "nonce", 4)
        self.log(f"nonce: {nonce}", log4Debug)
        secret, secretUrl = self.createSqrSecret()
        url = url + secretUrl
        imgPath = self.genQrcodeImageAndPrint(url)
        yield f"URL: {url}"
        yield f"IMG: {imgPath}"
        if self.checkQrCodeVerified(sqr):
            try:
                self.verifyCertificate(sqr, self.getSqrCert())
            except:
                c = self.createPinCode(sqr)
                yield f"請輸入pincode: {c}"
                self.checkPinCodeVerified(sqr)
            e = self.qrCodeLoginV2ForSecure(
                sqr, self.MODEL_NAME, self.USERDOMAIN, nonce
            )
            self.log(e, log4Debug)
            cert = self.checkAndGetValue(e, "certificate", 1)
            self.saveSqrCert(cert)
            tokenV3Info = self.checkAndGetValue(e, "tokenV3IssueResult", 3)
            _mid = self.checkAndGetValue(e, "mid", 4)
            metadata = self.checkAndGetValue(e, "metaData", 10)
            self.decodeE2EEKeyV1(metadata, secret, _mid)
            authToken = self.checkAndGetValue(tokenV3Info, "accessToken", 1)
            refreshToken = self.checkAndGetValue(tokenV3Info, "refreshToken", 2)
            self.saveCacheData(".refreshToken", authToken, refreshToken)
            print(f"AuthToken: {authToken}")
            print(f"RefreshToken: {refreshToken}")
            if isSelf:
                self.authToken = authToken
            yield authToken
            return
        raise Exception("can not check qr code, try again?")

    def createSession(self):
        """Create SQR session."""
        params = []
        sqrd = self.generateDummyProtocol("createSession", params, 4)
        return self.postPackDataAndGetUnpackRespData("/acct/lgn/sq/v1", sqrd, 4)

    def createQrCode(self, qrcode):
        params = [[12, 1, [[11, 1, qrcode]]]]
        sqrd = self.generateDummyProtocol("createQrCode", params, 3)
        return self.postPackDataAndGetUnpackRespData("/acct/lgn/sq/v1", sqrd, 3)

    def checkQrCodeVerified(self, qrcode):
        params = [
            [
                12,
                1,
                [
                    [11, 1, qrcode],
                ],
            ],
        ]
        sqrd = self.generateDummyProtocol("checkQrCodeVerified", params, 3)
        headers = self.server.additionalHeaders(
            self.server.Headers, {"x-lst": "150000"}  # timeout
        )
        try:
            self.postPackDataAndGetUnpackRespData(
                "/acct/lp/lgn/sq/v1",
                sqrd,
                3,
                headers=headers,
                access_token=qrcode,
                conn=requests.session(),
            )
        except Exception as e:
            print(f"[checkQrCodeVerified] {e}")
            return False
        return True

    def verifyCertificate(self, qrcode, cert=None):
        params = [
            [
                12,
                1,
                [
                    [11, 1, qrcode],
                    [11, 2, cert],
                ],
            ],
        ]
        sqrd = self.generateDummyProtocol("verifyCertificate", params, 3)
        return self.postPackDataAndGetUnpackRespData(
            self.LINE_SECONDARY_QR_LOGIN_ENDPOINT, sqrd, 3
        )

    def createPinCode(self, qrcode):
        params = [
            [
                12,
                1,
                [
                    [11, 1, qrcode],
                ],
            ],
        ]
        sqrd = self.generateDummyProtocol("createPinCode", params, 3)
        return self.postPackDataAndGetUnpackRespData("/acct/lgn/sq/v1", sqrd, 3)

    def checkPinCodeVerified(self, qrcode):
        params = [
            [
                12,
                1,
                [
                    [11, 1, qrcode],
                ],
            ],
        ]
        sqrd = self.generateDummyProtocol("checkPinCodeVerified", params, 3)
        headers = self.server.additionalHeaders(
            self.server.Headers, {"x-lst": "150000"}  # timeout
        )
        try:
            self.postPackDataAndGetUnpackRespData(
                "/acct/lp/lgn/sq/v1",
                sqrd,
                3,
                headers=headers,
                access_token=qrcode,
                conn=requests.session(),
            )
        except Exception as e:
            print(f"[checkPinCodeVerified] {e}")
            return False
        return True

    def qrCodeLogin(
        self, authSessionId: str, secret: str, autoLoginIsRequired: bool = True
    ):
        params = [
            [
                12,
                1,
                [
                    [11, 1, authSessionId],
                    [11, 2, self.SYSTEM_NAME],
                    [2, 3, autoLoginIsRequired],
                ],
            ]
        ]
        sqrd = self.generateDummyProtocol("qrCodeLogin", params, 3)
        data = self.postPackDataAndGetUnpackRespData("/acct/lgn/sq/v1", sqrd, 3)
        pem = self.checkAndGetValue(data, 1, "val_1")
        self.saveSqrCert(pem)
        print("證書: ", pem)
        _token = self.checkAndGetValue(data, 2, "val_2")
        e2eeInfo = self.checkAndGetValue(data, 4, "val_4")
        _mid = self.checkAndGetValue(data, 5, "val_5")
        if e2eeInfo is not None:
            self.decodeE2EEKeyV1(e2eeInfo, secret, _mid)
        return _token

    def qrCodeLoginV2(
        self,
        authSessionId,
        modelName="彥彥好睡",
        systemName="鴻鴻好暈",
        autoLoginIsRequired=True,
    ):
        params = [
            [
                12,
                1,
                [
                    [11, 1, authSessionId],
                    [11, 2, systemName],
                    [11, 3, modelName],
                    [2, 4, autoLoginIsRequired],
                ],
            ]
        ]
        sqrd = self.generateDummyProtocol("qrCodeLoginV2", params, 3)
        return self.postPackDataAndGetUnpackRespData("/acct/lgn/sq/v1", sqrd, 3)

    def CPF(self):
        sqrd = []
        return self.postPackDataAndGetUnpackRespData("/CPF", sqrd)

    def getRSAKeyInfo(self, provider=1):
        """
        provider:
         - UNKNOWN(0),
         - LINE(1),
         - NAVER_KR(2),
         - LINE_PHONE(3)
        """
        params = [
            [8, 2, provider],
        ]
        sqrd = self.generateDummyProtocol("getRSAKeyInfo", params, 3)
        return self.postPackDataAndGetUnpackRespData("/api/v3/TalkService.do", sqrd, 3)

    def loginV2(
        self,
        keynm,
        encData,
        secret,
        deviceName="Chrome",
        cert=None,
        verifier=None,
        calledName="loginV2",
    ):
        loginType = 2
        if secret is None:
            loginType = 0
        if verifier is not None:
            loginType = 1
        params = [
            [
                12,
                2,
                [
                    [8, 1, loginType],
                    [8, 2, 1],  # provider
                    [11, 3, keynm],
                    [11, 4, encData],
                    [2, 5, 0],
                    [11, 6, ""],
                    [11, 7, deviceName],
                    [11, 8, cert],
                    [11, 9, verifier],
                    [11, 10, secret],
                    [8, 11, 1],
                    [11, 12, "System Product Name"],
                ],
            ]
        ]
        sqrd = self.generateDummyProtocol(calledName, params, 3)
        return self.postPackDataAndGetUnpackRespData("/api/v3p/rs", sqrd, 3)

    def loginZ(
        self,
        keynm,
        encData,
        systemName="DeachSword-2021",
        certificate=None,
        verifier=None,
    ):
        sqrd = [128, 1, 0, 1] + self.getStringBytes("loginZ") + [0, 0, 0, 0]
        sqrd += [12, 0, 2]
        loginType = 0
        if verifier is not None:
            loginType = 1
        sqrd += [8, 0, 1] + self.getIntBytes(loginType)  # 2 if e2ee
        sqrd += [8, 0, 2] + self.getIntBytes(1)  # provider
        sqrd += [11, 0, 3] + self.getStringBytes(keynm)
        sqrd += [11, 0, 4] + self.getStringBytes(encData)
        sqrd += [2, 0, 5, 0]
        sqrd += [11, 0, 6] + self.getStringBytes("")  # accessLocation
        sqrd += [11, 0, 7] + self.getStringBytes(systemName)
        sqrd += [11, 0, 8] + self.getStringBytes(certificate)
        if verifier is not None:
            sqrd += [11, 0, 9] + self.getStringBytes(verifier)
        # sqrd += [11, 0, 10] + self.getStringBytes("") #secret
        sqrd += [8, 0, 11] + self.getIntBytes(1)
        sqrd += [0, 0]
        return self.postPackDataAndGetUnpackRespData("/api/v3p/rs", sqrd, 3)

    def checkLoginZPinCode(self, accessSession):
        hr = self.server.additionalHeaders(self.server.Headers, {"x-lhm": "GET"})
        return self.postPackDataAndGetUnpackRespData(
            self.SECONDARY_DEVICE_LOGIN_VERIFY_PIN,
            [],
            -3,
            headers=hr,
            access_token=accessSession,
            conn=requests.session(),
        )["result"]

    def checkLoginV2PinCode(self, accessSession):
        hr = self.server.additionalHeaders(self.server.Headers, {"x-lhm": "GET"})
        return self.postPackDataAndGetUnpackRespData(
            self.SECONDARY_DEVICE_LOGIN_VERIFY_PIN_WITH_E2EE,
            [],
            -3,
            headers=hr,
            access_token=accessSession,
            conn=requests.session(),
        )["result"]

    def testTBinary(self):
        METHOD_NAME = "getProfile"
        params = []
        sqrd = self.generateDummyProtocol(METHOD_NAME, params, 3)
        res = self.postPackDataAndGetUnpackRespData("/S3", sqrd, -1)
        return res

    def testTCompact(self):
        METHOD_NAME = "getProfile"
        params = []
        sqrd = self.generateDummyProtocol(METHOD_NAME, params, 4)
        res = self.postPackDataAndGetUnpackRespData("/S4", sqrd, -1)
        return res

    def testTMoreCompact(self):
        METHOD_NAME = "getProfile"
        params = []
        sqrd = self.generateDummyProtocol(METHOD_NAME, params, 4)
        res = self.postPackDataAndGetUnpackRespData("/S5", sqrd, -1)
        return res
