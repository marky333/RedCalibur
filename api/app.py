from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from redcalibur.config import Config, setup_logging
from redcalibur.osint.domain_infrastructure.whois_lookup import perform_whois_lookup
from redcalibur.osint.domain_infrastructure.dns_enumeration import enumerate_dns_records
from redcalibur.osint.domain_infrastructure.subdomain_discovery import discover_subdomains
from redcalibur.osint.domain_infrastructure.port_scanning import perform_port_scan
from redcalibur.osint.domain_infrastructure.ssl_tls_details import get_ssl_details
from redcalibur.osint.network_threat_intel.shodan_integration import perform_shodan_scan
from redcalibur.osint.user_identity.username_lookup import lookup_username
from redcalibur.osint.virustotal_integration import scan_url
from redcalibur.osint.ai_enhanced.recon_summarizer import summarize_recon_data
from redcalibur.osint.ai_enhanced.risk_scoring import calculate_risk_score

logger = setup_logging()
config = Config()

app = FastAPI(title="RedCalibur API", version="0.1.0")

# CORS for dev convenience
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DomainRequest(BaseModel):
    target: str
    whois: bool = False
    dns: bool = False
    subdomains: bool = False
    ssl: bool = False
    all: bool = False


class ScanRequest(BaseModel):
    target: str
    ports: Optional[List[int]] = None
    shodan: bool = False


class UsernameRequest(BaseModel):
    target: str
    platforms: Optional[List[str]] = None


class URLScanRequest(BaseModel):
    url: str


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.post("/domain")
def domain_recon(req: DomainRequest):
    results: Dict[str, Any] = {"target": req.target, "timestamp": datetime.now().isoformat()}
    errors: Dict[str, Any] = {}

    # WHOIS
    if req.whois or req.all:
        try:
            results["whois"] = perform_whois_lookup(req.target)
        except Exception as e:
            logger.error(f"WHOIS error: {e}")
            errors["whois"] = str(e)

    # DNS
    if req.dns or req.all:
        try:
            results["dns"] = enumerate_dns_records(req.target)
        except Exception as e:
            logger.error(f"DNS error: {e}")
            errors["dns"] = str(e)

    # Subdomains
    if req.subdomains or req.all:
        try:
            results["subdomains"] = discover_subdomains(req.target, config.SUBDOMAIN_WORDLIST)
        except Exception as e:
            logger.error(f"Subdomain discovery error: {e}")
            errors["subdomains"] = str(e)

    # SSL
    if req.ssl or req.all:
        try:
            results["ssl"] = get_ssl_details(req.target)
        except Exception as e:
            logger.error(f"SSL details error: {e}")
            errors["ssl"] = str(e)

    # AI enrichment (optional)
    if req.all:
        try:
            import json
            raw_data = json.dumps(results, indent=2, default=str)
            results["ai_summary"] = summarize_recon_data(raw_data[:2000])
            features = [
                len(results.get("subdomains", [])),
                1 if isinstance(results.get("ssl", {}), dict) and "error" not in results.get("ssl", {}) else 0,
                len(results.get("dns", {}).get("A", [])) if isinstance(results.get("dns", {}), dict) else 0,
            ]
            results["risk_score"] = calculate_risk_score(features)
        except Exception as e:
            logger.error(f"AI enrichment failed: {e}")
            errors["ai"] = str(e)

    if errors:
        results["errors"] = errors
    return results


@app.post("/scan")
def scan(req: ScanRequest):
    results: Dict[str, Any] = {"target": req.target, "timestamp": datetime.now().isoformat()}
    try:
        ports = req.ports or config.DEFAULT_PORTS
        results["port_scan"] = perform_port_scan(req.target, ports)
        if req.shodan:
            if not config.SHODAN_API_KEY:
                results["shodan_error"] = "SHODAN_API_KEY not configured"
            else:
                results["shodan"] = perform_shodan_scan(config.SHODAN_API_KEY, req.target)
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return results


@app.post("/username")
def username(req: UsernameRequest):
    try:
        platforms = req.platforms or ["twitter", "linkedin", "github", "instagram"]
        return {
            "target": req.target,
            "timestamp": datetime.now().isoformat(),
            "username_lookup": lookup_username(req.target, platforms),
        }
    except Exception as e:
        logger.error(f"Username lookup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/urlscan")
def urlscan(req: URLScanRequest):
    try:
        if not config.VIRUSTOTAL_API_KEY:
            raise HTTPException(status_code=400, detail="VIRUSTOTAL_API_KEY not configured")
        data = scan_url(config.VIRUSTOTAL_API_KEY, req.url)
        if not data:
            raise HTTPException(status_code=502, detail="VirusTotal returned no data")
        return data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"URL scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class SummarizeRequest(BaseModel):
    payload: Dict[str, Any]


@app.post("/summarize")
def summarize(req: SummarizeRequest):
    try:
        import json
        raw = json.dumps(req.payload, indent=2, default=str)
        return {"summary": summarize_recon_data(raw[:4000])}
    except Exception as e:
        logger.error(f"Summarize failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
