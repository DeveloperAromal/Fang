# Fang

An autonomous AI-powered reconnaissance framework for bug bounty hunters and security researchers.

Most recon tools give you raw data and leave you to figure out the rest. Fang runs the recon, reasons over the findings, and tells you what matters.

---

## How it works

You type a plain English objective. Fang handles everything else.

```
> scan testfire.net for open ports, technologies, and any potential vulnerabilities
```

```
[*] Target: https://testfire.net
[+] scan_ports completed
[+] grab_banners completed
[+] fingerprint_tech completed
[+] parse_robots completed
[+] crawl_urls completed
[+] scrape_web completed
[*] Analyzing findings...
[+] Analysis complete
[*] Generating report...
[+] Report saved -> reports/report_20250309_142301.md
```

---

## Architecture

```
User prompt
    |
Planner (LLM)         -- decides which tools to run and in what order
    |
Orchestrator          -- executes the tool pipeline with dependency resolution
    |
STORAGE               -- holds all raw findings in memory
    |
Analyzer (LLM)        -- reasons over findings, assigns severities, maps CVEs
    |
Report Generator      -- produces a professional markdown report
```

---

## Tools

| Tool | Description |
|------|-------------|
| `scan_ports` | Scan open TCP ports and detect running services |
| `grab_banners` | Grab service banners to identify versions (runs after port scan) |
| `fingerprint_tech` | Detect CMS, frameworks, servers, and JS libraries |
| `parse_robots` | Parse robots.txt to reveal disallowed paths and hidden endpoints |
| `crawl_urls` | Crawl the target site and map all discoverable endpoints |
| `scrape_web` | Scrape raw HTML for comments, metadata, and exposed data |
| `enumerate_subdomains` | Enumerate subdomains using a wordlist |
| `domain_details` | Gather WHOIS, DNS records, registrar, and IP info |
| `social_media_osint` | Extract social media presence linked to the target |

---

## AI Pipeline

**Planner** reads your objective in natural language, selects only the relevant tools, infers the target URL, and resolves execution order automatically.

**Analyzer** takes the raw recon output and produces a structured threat assessment with severity ratings (CRITICAL, HIGH, MEDIUM, LOW, INFO), CVE mappings, attack surface identification, and remediation recommendations.

**Report Generator** converts the analysis into a professional penetration testing report in markdown — ready to submit for bug bounties or hand to clients.

---

## Installation

```bash
git clone https://github.com/DeveloperAromal/Fang.git
cd Fang
pip install -r requirements.txt
```

---


## Usage

```bash
python main.py
```
or
```bash
chmod +x fang.sh
./fang.sh
```

```
> scan example.com for subdomains and open ports
> scan https://target.com for technologies and vulnerabilities
> full recon on example.com
> exit
```

Reports are saved to the `reports/` directory.

---

<img src="https://github.com/DeveloperAromal/Fang/blob/main/assets/fang_scr.png" alt="scr"/>

## Project Structure


```
Fang
├─ assets
│  └─ fang_scr.png
├─ config
│  └─ settings.py
├─ docs
├─ fang
│  ├─ agent
│  │  ├─ orchestrator.py
│  │  ├─ planner
│  │  │  └─ planner.py
│  │  └─ prompt
│  │     └─ agent_prompt.py
│  ├─ data
│  │  ├─ ports.json
│  │  └─ subdomain_list.txt
│  ├─ memory
│  │  └─ storage.py
│  ├─ modules
│  │  ├─ network
│  │  │  ├─ capture_banner.py
│  │  │  └─ port_scanner.py
│  │  └─ web
│  │     ├─ basic
│  │     │  ├─ robots_parser.py
│  │     │  ├─ subdomain_enumerator.py
│  │     │  ├─ tech_fingerprint.py
│  │     │  ├─ url_crawler.py
│  │     │  ├─ web_scrapper.py
│  │     │  └─ __init__.py
│  │     └─ osint
│  │        ├─ domain_details.py
│  │        └─ social_media_data_extracter.py
│  ├─ report
│  │  ├─ analyser.py
│  │  ├─ report_generator.py
│  │  └─ template
│  │     └─ template_report.md
│  └─ utils
│     ├─ banner.py
│     ├─ config_helpers.py
│     ├─ ip_data.py
│     ├─ json_cleaner.py
│     ├─ logger.py
│     ├─ memory_filter.py
│     └─ prompt_fn.py
├─ fang.sh
├─ generated
├─ LICENSE
├─ main.py
├─ README.md
└─ requirements.txt

```
---

## Disclaimer

Fang is built for authorized security testing and bug bounty hunting only. Only scan targets you have explicit permission to test. The authors are not responsible for any misuse.

---

## Author

Built by [Aromal](https://github.com/DeveloperAromal)

Star the repo if you find it useful. Follow on GitHub for updates.

https://github.com/DeveloperAromal/Fang
