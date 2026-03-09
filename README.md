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

## Configuration

Edit `config/settings.py` and fill in your LLM credentials:

```python
LLM_PROVIDER = "openai"
LLM_API_KEY  = "your-api-key"
LLM_MODEL    = "gpt-4o"
LLM_BASE_URL = "https://api.openai.com/v1"
```

---

## Usage

```bash
python main.py
```

```
> scan example.com for subdomains and open ports
> scan https://target.com for technologies and vulnerabilities
> full recon on example.com
> exit
```

Reports are saved to the `reports/` directory.

---

## Project Structure

```
Fang
├── config
│   └── settings.py           # LLM config, tool registry, scan settings
├── fang
│   ├── agent
│   │   ├── orchestrator.py   # Connects planner -> tools -> analyzer
│   │   ├── planner           # LLM-powered tool selector
│   │   └── prompt            # All LLM prompts
│   ├── data
│   │   ├── ports.json
│   │   └── subdomain_list.txt
│   ├── memory
│   │   └── storage.py        # In-memory findings store
│   ├── modules
│   │   ├── network           # Port scanner, banner grabber
│   │   └── web
│   │       ├── basic         # Robots, subdomains, tech, crawler, scraper
│   │       └── osint         # Domain details, social media
│   ├── report
│   │   ├── analyser.py       # AI vulnerability analyzer
│   │   └── report_generator.py
│   └── utils
│       ├── banner.py
│       ├── logger.py
│       └── ip_data.py
├── reports                   # Generated reports saved here
└── main.py
```

---

## Disclaimer

Fang is built for authorized security testing and bug bounty hunting only. Only scan targets you have explicit permission to test. The authors are not responsible for any misuse.

---

## Author

Built by [Aromal](https://github.com/DeveloperAromal)

Star the repo if you find it useful. Follow on GitHub for updates.

https://github.com/DeveloperAromal/Fang
