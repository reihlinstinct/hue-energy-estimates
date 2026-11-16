# Hue energy estimates: proposed design

Status: design only. Collection, OAuth linking and workflows are disabled.

## Goal

Estimate electricity used by Hue lighting from observed states, model-specific power profiles and time. This is not a meter reading and not a claim of complete historical consumption.

## Architecture

1. A one-time OAuth setup links a Hue account with an internet-connected Hue Bridge to a registered developer app.
2. A GitHub-hosted job reads authorized light resources through Hue Remote API using HTTPS.
3. The collector validates a strict allowlist of state fields, applies model-specific power profiles, and encrypts records to an owner-held public encryption key before persistent storage.
4. Reports decrypt only in an authorized private environment. Public repository files and job output contain no household data.

A normal cloud runner cannot reach the private home-network Bridge address. Do not expose the Bridge to the internet. A continuously running local collector is a separate possible design, not part of this first version.

## Authority and scope

- Read lighting state only. No light switching, dimming, scene recalls, sensor reconfiguration or automation writes.
- Setup necessarily creates credentials and authorizes the application. These setup mutations must be separated from the runtime GET-only transport.
- If Hue cannot issue vendor-enforced read-only authorization, state that clearly before linking. Enforce read-only runtime methods in code and tests; do not describe this as least-privilege OAuth if it is not.
- No paid services, runner classes, storage upgrades or new hardware. Stop on cost requirements, throttling or challenges.
- Do not register newsletter subscriptions.

## Observed fields

Start with opaque light identifier, model identifier, reachable/connected state, on/off state, brightness, available color/color-temperature fields and observation timestamp. Each field must be confirmed against current authorized official docs. No names, rooms, geolocation, account email, motion data, temperature data, automations or full API payloads are needed for the energy goal.

Identifiers and household usage remain private even without names. Never print response bodies, headers, tokens, OAuth codes or decrypted samples.

## Energy model

Prefer measured lookup curves for the exact device model, accounting for brightness and color where supported. Use standby power only where grounded for the model and distinguish wall-power-off/unreachable from command-off standby. Unknown model profiles produce unavailable estimates, not an invented generic wattage. If nominal-power fallback is later offered, label it a coarse assumption and keep it separate from profile-based estimates.

Integrate estimated watts over observed intervals. Never treat an observed state as proof of the entire preceding or following interval. Retain the assumption, observation spacing, missing samples and profile source/version with the result. Publish an observation-based estimate, coverage and an uncertainty warning, not an exact daily total.

No full past-use backfill is promised. A fridge-style hourly poll can miss complete lighting sessions. GitHub schedules have a five-minute minimum and are not a continuous event recorder. Choose an initial cadence only after explicitly disclosing missing-transition risk; faster cloud-account polling requires the user's agreement after explaining account risk. Start with hourly unless separately approved.

## Privacy and secret storage

Public repository: source, design, synthetic fixtures and tests only. Private encrypted records: separate owner-approved destination. No real identifiers, usage timestamps, household names, application secrets or encryption private keys in commits, artifacts or logs.

Credentials belong in approved secret storage, never messages or repository files. OAuth access and refresh token lifetimes/rotation remain to verify. If refresh tokens rotate, serialize collection and persist rotation securely and atomically; do not enable a scheduled workflow until a tested storage route exists. A GitHub token capable of writing secrets is sensitive and must not be added casually.

Use authenticated encryption with a versioned schema and owner-held decryption key. Do not reuse another project's private key without an explicit reviewed decision. Consider fixed-size records to limit inference from encrypted file sizes. Restrict retention and avoid public timing/activity leakage even when payloads are encrypted.

## Cost controls

Public standard GitHub runners may be used for code and tests. Private runners/retention can exceed free quotas, so check account limits and prevent spending before any scheduled collection. No paid resources are approved. Disabled-by-default workflow until all controls are in place.

## Failure behavior

On expired/revoked authorization, invalid payload, unsupported model, unreachable Bridge, missing profile, stale sample, storage failure or throttling: record only a safe fixed status and a gap. Do not invent zero consumption, retry aggressively, alter lights or expose payloads. Stop collection on throttling pending review.

## Test and review gates

- Synthetic fixtures only, including false/zero, absent fields, NaN/infinite values, negative/invalid data and unknown fields.
- Runtime transport denies all mutation methods and unapproved hosts/redirects.
- Secret-canary tests for stdout/stderr, errors, snapshots and artifacts.
- Encryption round trip, wrong-key failure and old-version handling.
- Integration cases for gaps, stale data, offline devices, unknown profiles and token rotation without real credentials.
- Private-data scan before publication; independent review and green exact-head CI before enablement.

## Open checks before implementation

1. Current remote registration approval process and absence of charges.
2. Actual OAuth consent permissions, resource coverage and revocation route.
3. Token expiration/rotation and safe free persistence.
4. Authorized encrypted-log destination and key setup.
5. Exact model inventory and power-profile licensing/provenance.
6. Collection cadence and declared limits of observation-based estimates.

## Sources

- https://developers.meethue.com/develop/get-started-2/
- https://developers.meethue.com/explore/why-develop-for-hue/
- https://developers.meethue.com/terms-of-use-and-conditions/
- https://developers.meethue.com/new-hue-api/
- https://developers.meethue.com/Philips%20Hue%20-%20Sustainability%20-%20Whitepaper.pdf
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
