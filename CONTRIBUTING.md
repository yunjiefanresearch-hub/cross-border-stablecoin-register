{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/stablecoin-rail-register/schema/record.schema.json",
  "title": "Stablecoin Rail Register — obligation record",
  "description": "One verified (jurisdiction x instrument x dimension) regulatory fact, versioned and sourced.",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "jurisdiction", "authority", "instrument_type", "dimension",
               "requirement_summary", "status", "source", "confidence",
               "last_reviewed", "version_added"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z]{2}-[a-z_]+-[a-z_]+-[0-9]{3}$",
      "description": "Stable id, e.g. hk-frs-permitted_activity_yield-001"
    },
    "jurisdiction": {
      "type": "string",
      "enum": ["HK", "TW", "BR", "US", "EU", "UK", "SG", "CN"]
    },
    "authority": { "type": "string", "minLength": 2 },
    "instrument_type": {
      "type": "string",
      "enum": ["fiat_referenced_stablecoin", "payment_stablecoin", "e_money_token",
               "asset_referenced_token", "tokenized_mmf", "tokenized_security", "other"]
    },
    "instrument_label_local": { "type": "string" },
    "dimension": {
      "type": "string",
      "enum": ["regulatory_authority", "issuer_pathway", "reserve_capital",
               "permitted_activity_yield", "redemption", "custody",
               "aml_kyc", "cross_border_data", "distribution", "implementation_status"]
    },
    "requirement_summary": { "type": "string", "minLength": 1 },
    "requirement_structured": { "type": "object", "additionalProperties": true },
    "status": { "type": "string", "enum": ["in_force", "transitional", "proposed", "consultation"] },
    "effective_date": { "type": ["string", "null"], "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
    "source": {
      "type": "object",
      "additionalProperties": false,
      "required": ["primary"],
      "properties": {
        "primary": { "type": "string", "minLength": 3 },
        "url": { "type": "string", "format": "uri" },
        "pinpoint": { "type": "string" }
      }
    },
    "secondary": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["citation"],
        "properties": {
          "citation": { "type": "string" },
          "url": { "type": "string", "format": "uri" }
        }
      }
    },
    "interpretation_note": { "type": "string" },
    "confidence": { "type": "string", "enum": ["high", "medium", "low"] },
    "last_reviewed": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
    "version_added": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "tags": { "type": "array", "items": { "type": "string" } }
  }
}
