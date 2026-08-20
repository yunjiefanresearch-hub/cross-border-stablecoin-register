"""Controlled public catalog values shared by the API and MCP surface."""

DIMENSIONS: dict[str, str] = {
    "regulatory_authority": "Authority and statutory basis",
    "issuer_pathway": "Issuer eligibility / licensing pathway (constraint C1)",
    "reserve_backing": "Reserve composition and backing (constraint C2)",
    "capital_requirements": "Issuer capital requirements (constraint C2)",
    "permitted_activity_yield": "Permitted-activity / yield boundary — SPINE 1 (constraint C3)",
    "securities_classification": "Securities classification boundary — SPINE 2 (constraint C4)",
    "bank_nonbank_routing": "Bank / non-bank status and routing prohibitions (constraint C5)",
    "redemption": "Redemption mechanics",
    "custody": "Custody of client assets / reserves (constraint C2 facet)",
    "aml_kyc": "AML / KYC framework",
    "cross_border_data": "Cross-border payment and data sovereignty (constraint C6)",
    "monetary_sovereignty": "Monetary sovereignty / non-domestic-currency caps (constraint C7)",
    "disclosure_reporting": "Disclosure, reporting, supervisory coordination (constraint C8)",
    "distribution": "Distribution and offering restrictions",
    "implementation_status": "Implementation maturity and timeline",
}

JURISDICTIONS: dict[str, str] = {
    "US": "United States",
    "HK": "Hong Kong",
    "EU": "European Union",
    "UK": "United Kingdom",
    "SG": "Singapore",
    "CN": "Mainland China",
    "BR": "Brazil",
    "CH": "Switzerland",
    "AE": "United Arab Emirates",
    "TW": "Taiwan",
    "JP": "Japan",
    "KR": "South Korea",
}
