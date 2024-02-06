# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from contextlib import suppress
from Kekik.cli  import konsol
from typing     import Literal

from os import name as _sistem
from subprocess import Popen

from os import environ
environ["WDM_LOG"] = "0"

from logging import getLogger, NOTSET
wdm_log = getLogger("WDM")
wdm_log.setLevel(NOTSET)
with suppress(Exception):
    wdm_log.removeHandler(wdm_log.handlers[0])

from webdriver_manager.chrome          import ChromeDriverManager
from selenium.webdriver                import Chrome, ChromeOptions, Remote
from selenium.webdriver.chrome.service import Service
from random  import randint
from zipfile import ZipFile
from json    import loads

from selenium.webdriver.support.ui           import WebDriverWait
from selenium.webdriver.support              import expected_conditions as EC
from selenium.webdriver.common.by            import By
from selenium.webdriver.remote.webelement    import WebElement
from selenium.webdriver.common.keys          import Keys
from selenium.webdriver.common.action_chains import ActionChains

from parsel import Selector

class SelSik:
    def tarayici_kapat(self):
        with suppress(Exception):
            self.tarayici.delete_all_cookies()
        with suppress(Exception):
            self.tarayici.execute_cdp_cmd(
                "Storage.clearDataForOrigin", {
                    "origin"       : "*",
                    "storageTypes" : "all",
                }
            )

        with suppress(Exception):
            self.tarayici.close()

        with suppress(Exception):
            self.tarayici.execute_script("window.close();")

        with suppress(Exception):
            self.tarayici.quit()

        if _sistem != "nt":
            with suppress(Exception):
                Popen("rm -rf /tmp/.com.google.Chrome.*", shell=True)

    def __init__(
        self,
        link:str,
        proxi:str     = None,
        pencere:Literal["normal", "kiosk", "uygulama", "gizli"] = "uygulama",
        foto:bool     = True,
        genislik:int  = 750,
        yukseklik:int = 750,
        enlem:int     = 600,
        boylam:int    = 0,
        kimlik:str    = None,
        gizlilik:bool = True,
        minimize:bool = False,
        chrome_v:str  = None,
        remote:str    = None,
        data_dir:str  = None
    ):
        self.options = ChromeOptions()
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.options.add_experimental_option("detach", False)
        self.options.add_experimental_option("prefs", {
            "intl.accept_languages"                           : "en,en_US",
            # "profile.managed_default_content_settings.images" : 2,         # ! Fotoğraflar Devredışı
            "credentials_enable_service"                      : False,
            "profile.password_manager_enabled"                : False,
        })
        if not foto:
            self.options.add_argument('--blink-settings=imagesEnabled=false')  # ! Fotoğraflar Devredışı
        self.options.add_argument("--lang=en-US")
        self.options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--mute-audio")
        self.options.add_argument("--enable-webgl-draft-extensions")
        self.options.add_argument("--ignore-gpu-blocklist")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-password-manager-reauthentication")
        self.options.add_argument(f"--window-position={enlem},{boylam}")
        self.options.add_argument(f"--window-size={genislik},{yukseklik}")
        self.options.add_argument("--allow-insecure-localhost")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--remote-debugging-port=9222")
        if data_dir:
            self.options.add_argument(f"--user-data-dir={data_dir}")

        match pencere:
            case "normal":
                self.options.headless = False
            case "uygulama":
                self.options.add_experimental_option("mobileEmulation", {"deviceMetrics": { "width": genislik, "height": yukseklik, "pixelRatio": 3.0 }})
                self.options.add_argument("--app=https://httpbin.org/ip")
            case "kiosk":
                self.options.add_argument("--kiosk=https://httpbin.org/ip")
            case "gizli":
                self.options.headless = True

        if kimlik:
            self.options.add_argument(f"--user-agent={kimlik}")

        auth_proxy = None
        if proxi:
            if auth_proxy := len(proxi.split(":")) == 4:
                eklenti = self.__proxi_eklenti(proxi)
                self.options.add_extension(eklenti)
            else:
                self.options.add_argument(f"--proxy-server={proxi}")


        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL", "network": "ALL"})
        self.options.set_capability("acceptInsecureCerts", True)

        if not remote:
            servis = Service(ChromeDriverManager(chrome_v).install())

        if _sistem == "nt":
            from subprocess import CREATE_NO_WINDOW
            servis.creation_flags = CREATE_NO_WINDOW

        if not remote:
            self.tarayici = Chrome(service=servis, options=self.options)
        else:
            self.tarayici = Remote(command_executor=remote, options=self.options)

        if minimize:
            self.tarayici.minimize_window()

        if gizlilik and not remote:
            from selenium_stealth import stealth
            stealth(
                driver       = self.tarayici,
                user_agent   = kimlik,
                languages    = ["en-US", "en"],
                vendor       = "Google Inc.",
                platform     = "Win32",
                webgl_vendor = "Google Inc. (Intel)",
                renderer     = "ANGLE (Intel, Mesa Intel(R) Xe Graphics (TGL GT2), OpenGL 4.6)",
                fix_hairline = True,
            )

        if auth_proxy:
            try:
                self.tarayici.get("https://httpbin.org/ip")
                self.tarayici.get(link)
            except Exception as hata:
                konsol.log(f"[{type(hata).__name__}] {hata}")
                self.tarayici.close()

            from os import remove
            with suppress(FileNotFoundError):
                remove(eklenti)

        if not proxi:
            self.tarayici.get(link)

        self.remote = remote

    def __proxi_eklenti(self, proxi_str:str) -> str:
        _host, _port, _user, _pass = proxi_str.split(":")

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "KekikProxi",
            "description": "Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.",
            "author": {
                "name": "keyiflerolsun",
                "email": "keyiflerolsun@gmail.com"
            },
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """ % (_host, _port, _user, _pass)

        pluginfile = f'KekikProxi_{randint(0,999)}.zip'

        with ZipFile(pluginfile, 'w') as dosya:
            dosya.writestr("manifest.json", manifest_json)
            dosya.writestr("background.js", background_js)

        return pluginfile

    def __tampermonkey(self, greasyfork_link:str) -> None:
        tampermonkey = "Tampermonkey.crx"

        from os.path import isfile
        if not isfile(tampermonkey):
            raise FileNotFoundError(tampermonkey)

        self.options.add_extension(tampermonkey)

        WebDriverWait(self.tarayici, 5).until(EC.number_of_windows_to_be(2))
        self.tarayici.switch_to.window(self.tarayici.window_handles[1])

        self.tarayici.get(greasyfork_link)
        self.bekle_tikla("//*[@id='install-area']/a[1]")

        WebDriverWait(self.tarayici, 5).until(EC.number_of_windows_to_be(3))
        self.tarayici.switch_to.window(self.tarayici.window_handles[2])
        self.bekle_tikla("//*[@value='Kur']")

        self.tarayici.switch_to.window(self.tarayici.window_handles[1])
        self.tarayici.close()

        self.tarayici.switch_to.window(self.tarayici.window_handles[0])

    @property
    def _headers(self) -> dict:
        js_headers = """
            const _xhr = new XMLHttpRequest();
            _xhr.open("HEAD", document.location, false);
            _xhr.send(null);
            const _headers = {};
            _xhr.getAllResponseHeaders().trim().split(/[\\r\\n]+/).map((value) => value.split(/: /)).forEach((keyValue) => {
                _headers[keyValue[0].trim()] = keyValue[1].trim();
            });
            return _headers;
        """
        return self.tarayici.execute_script(js_headers)

    @property
    def _kurabiyeler(self) -> dict:
        return {kurabiye["name"]: kurabiye["value"] for kurabiye in self.tarayici.get_cookies()}

    def xhr_ver(self, arama_metni:str=None, arama_linki:str=None) -> list[dict | None]:
        raw_logs = self.tarayici.get_log("performance")

        if arama_metni:
            return [loads(log["message"]) for log in raw_logs if arama_metni in log["message"]]

        mesaj_logs = [loads(raw_log["message"])["message"] for raw_log in raw_logs]
        json_logs  = [json_log for json_log in mesaj_logs if json_log["method"] == "Network.responseReceived" and "json" in json_log["params"]["response"]["mimeType"]]

        for log in json_logs:
            if arama_linki in log["params"]["response"]["url"]:
                return loads(self.tarayici.execute_cdp_cmd("Network.getResponseBody", {"requestId": log["params"]["requestId"]})["body"])

    def xpath(self, xpath:str) -> WebElement:
        return self.tarayici.find_element(By.XPATH, xpath)

    def kaynak_kod(self, xpath:str) -> Selector:
        return Selector(self.tarayici.page_source).xpath(xpath)
        # * return Selector(self.tarayici.execute_script("return document.body.innerHTML;")).xpath(xpath)
        # * return Selector(self.xpath(xpath).get_attribute('innerHTML'))

    def eleman_bekle(self, secici:str, saniye:int=10, by=By.XPATH) -> WebElement | None:
        try:
            WebDriverWait(self.tarayici, saniye).until(EC.presence_of_element_located((by, secici)))
            return self.tarayici.find_element(by, secici)
        except Exception:
            return None

    def mause_gotur(self, secici:str, by=By.XPATH) -> None:
        ActionChains(self.tarayici).move_to_element(self.eleman_bekle(secici, by=by)).perform()

    def bekle_tikla(self, secici:str, saniye:int=10, by=By.XPATH) -> WebElement | None:
        # * self.eleman_bekle(secici, saniye, by)
        # * self.tarayici.find_element(by, secici).click()
        WebDriverWait(self.tarayici, saniye).until(EC.element_to_be_clickable((by, secici))).click()
        try:
            return self.tarayici.find_element(by, secici)
        except Exception:
            return None

    def metin_yaz(self, metin:str, gecikme_ms:int=250) -> None:
        for line in metin.split('\n'):
            ActionChains(self.tarayici, duration=gecikme_ms).send_keys(line).perform()
            ActionChains(self.tarayici).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        ActionChains(self.tarayici).send_keys(Keys.RETURN).perform()

    def metin_yapistir(self) -> None:
        ActionChains(self.tarayici).send_keys(f'{Keys.CONTROL}v').perform()

    def ekran_goruntusu(self, secici:str, dosya_adi:str, by=By.XPATH) -> str:
        # dosya_adi = f"ScreenShots/{dosya_adi}"
        self.tarayici.find_element(by, secici).screenshot(dosya_adi)
        return dosya_adi