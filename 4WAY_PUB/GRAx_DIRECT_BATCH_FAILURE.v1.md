# Grax Direct-Batch Failure v1

Before the routed audit, a direct `brullama batch brullama-grax:8b` attempt
was made with `GRAx_AUDIT_PROMPT.v1.txt`, SHA-256
`40530fe0ac7d0df44911a2da667ee97b155587a34c038bbc29baca1032443fa2`.
The daemon rejected it before producing an audit response:

```text
400 Bad Request: Grax chat requires /api/generate route custody
```

No semantic result is claimed from this attempt. The later
`GRAx_AUDIT_RUN.v1/` used the repository's routed, source-bound review runner.
