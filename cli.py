#!/usr/bin/env python3
import argparse
from .scanner import Scanner
from .output import ReportWriter
from rich.console import Console

console = Console()

def build_parser():
    p = argparse.ArgumentParser(
        prog="webreconx",
        description="WebReconX - lightweight web reconnaissance and vulnerability scanner"
    )
    p.add_argument("-u", "--url", required=True, help="Target URL, e.g. https://example.com/")
    p.add_argument("--scan", default="all",
                   help="Comma-separated modules to run (all, subdomains, dirs, xss, sqli, lfi, openredirect, csrf)")
    p.add_argument("-w", "--wordlist", help="Wordlist for subdomain/dir brute-force")
    p.add_argument("-t", "--threads", type=int, default=10, help="Number of worker threads (default: 10)")
    p.add_argument("-o", "--output", help="Write JSON report to this file")
    p.add_argument("--html", help="Write HTML report to this file")
    p.add_argument("--timeout", type=float, default=8.0, help="Request timeout (seconds)")
    return p

def main():
    args = build_parser().parse_args()
    modules = [m.strip().lower() for m in args.scan.split(",")] if args.scan != "all" else "all"
    sc = Scanner(base_url=args.url, threads=args.threads, timeout=args.timeout, wordlist=args.wordlist)
    results = sc.run(modules)
    rw = ReportWriter(results, target=args.url)
    if args.output:
        rw.write_json(args.output)
        console.print(f"[green]JSON report saved to {args.output}[/green]")
    if args.html:
        rw.write_html(args.html)
        console.print(f"[green]HTML report saved to {args.html}[/green]")
    if not (args.output or args.html):
        # Pretty print to console
        from rich.table import Table
        table = Table(title=f"WebReconX Results for {args.url}")
        table.add_column("Module")
        table.add_column("Findings", justify="left")
        for mod, data in results.items():
            if isinstance(data, list):
                val = "\n".join(map(str, data)) if data else "-"
            else:
                val = json.dumps(data, ensure_ascii=False, indent=2)
            table.add_row(mod, val if val else "-")
        console.print(table)

if __name__ == "__main__":
    main()
