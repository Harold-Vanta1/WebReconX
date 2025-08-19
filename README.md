# **WebReconX**

WebReconX is a **lightweight web reconnaissance and vulnerability scanner** for bug bounty and pentest workflows.

## **Features**
- 🔎 Subdomain enumeration (DNS resolve-based)
- 📁 Directory enumeration (status-based)
- 🧪 XSS, SQLi, LFI, Open Redirect, CSRF heuristic checks
- 🧵 Multithreaded enumeration
- 🎨 Pretty console output (Rich)
- 🧾 JSON/HTML reporting

## **Install**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## **Usage**
```bash
python -m webreconx.cli -u https://example.com --scan all -t 10 --output report.json --html report.html
```
Run a subset
```bash
python -m webreconx.cli -u "https://example.com/search?q=test" --scan xss,sqli
```

## **Notes**
- Provide a wordlist with `-w` to enhance subdomain/dir brute-force.
- Heuristic scanners are **best-effort** and may produce false positives. Manually verify findings.

## **Project Structure**
```
webreconx/
  cli.py
  scanner.py
  utils.py
  output.py
  modules/
    subdomain_enum.py
    dir_enum.py
    xss_scanner.py
    sqli_scanner.py
    lfi_scanner.py
    open_redirect.py
    csrf_scanner.py
requirements.txt
setup.py
README.md
LICENSE
```

## **License**
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more information.

