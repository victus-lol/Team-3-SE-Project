# API Documentation

The complete OpenAPI 3.0 specification is available at [docs/openapi.yaml](openapi.yaml).

## Base URL
`/api`

## Response Envelopes

### Success
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

### Error
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided"
  }
}
```

