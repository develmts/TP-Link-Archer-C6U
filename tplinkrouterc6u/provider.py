from logging import Logger

from tplinkrouterc6u import TPLinkXDRClient
from tplinkrouterc6u.common.exception import ClientException
from tplinkrouterc6u.client.c6u import TplinkRouter
from tplinkrouterc6u.client.deco import TPLinkDecoClient
from tplinkrouterc6u.client_abstract import AbstractRouter
from tplinkrouterc6u.client.mr import TPLinkMRClient
from tplinkrouterc6u.client.ex import TPLinkEXClient
from tplinkrouterc6u.client.c5400x import TplinkC5400XRouter
from tplinkrouterc6u.client.c1200 import TplinkC1200Router
from tplinkrouterc6u.client.c80 import TplinkC80Router
from tplinkrouterc6u.client.vr import TPLinkVRClient


class TplinkRouterProvider:
    @staticmethod
    def get_client(host: str, password: str, username: str = 'admin', logger: Logger = None,
                   verify_ssl: bool = True, timeout: int = 30) -> AbstractRouter:
        for client in [TplinkC5400XRouter, TPLinkVRClient, TPLinkEXClient, TPLinkMRClient, TPLinkDecoClient,
                       TPLinkXDRClient, TplinkRouter, TplinkC80Router]:
            router = client(host, password, username, logger, verify_ssl, timeout)
            if router.supports():
                return router

        message = ('Login failed! Please check if your router local password is correct or '
                   'try to use web encrypted password instead. Check the documentation!')
        router = TplinkC1200Router(host, password, username, logger, verify_ssl, timeout)
        try:
            router.authorize()
            return router
        except Exception:
            pass

        for client in [TPLinkVRClient, TPLinkXDRClient]:
            router = client(host, password, username, None, verify_ssl, timeout)
            try:
                router.authorize()
                message = ('Your router might be supported by {}. Please open the issue here '
                           'https://github.com/AlexandrErohin/TP-Link-Archer-C6U').format(router.__class__)
                break
            except Exception:
                pass

        raise ClientException(message)
