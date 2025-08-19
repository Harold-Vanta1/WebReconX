from .modules.subdomain_enum import SubdomainEnumerator
from .modules.dir_enum import DirEnumerator
from .modules.xss_scanner import XSSScanner
from .modules.sqli_scanner import SQLIScanner
from .modules.lfi_scanner import LFIScanner
from .modules.open_redirect import OpenRedirectScanner
from .modules.csrf_scanner import CSRFScanner

class Scanner:
    def __init__(self, base_url: str, threads: int = 10, timeout: float = 8.0, wordlist: str | None = None):
        self.base_url = base_url
        self.threads = threads
        self.timeout = timeout
        self.wordlist = wordlist

    def run(self, modules="all"):
        results = {}
        mods = ["subdomains","dirs","xss","sqli","lfi","openredirect","csrf"] if modules == "all" else modules
        if "subdomains" in mods:
            results["subdomains"] = SubdomainEnumerator(self.base_url, self.wordlist, self.threads).run()
        if "dirs" in mods:
            results["dirs"] = DirEnumerator(self.base_url, self.wordlist, self.threads, self.timeout).run()
        if "xss" in mods:
            results["xss"] = XSSScanner(self.base_url, self.timeout).run()
        if "sqli" in mods:
            results["sqli"] = SQLIScanner(self.base_url, self.timeout).run()
        if "lfi" in mods:
            results["lfi"] = LFIScanner(self.base_url, self.timeout).run()
        if "openredirect" in mods:
            results["openredirect"] = OpenRedirectScanner(self.base_url, self.timeout).run()
        if "csrf" in mods:
            results["csrf"] = CSRFScanner(self.base_url, self.timeout).run()
        return results
