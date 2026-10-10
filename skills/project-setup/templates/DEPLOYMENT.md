# Deployment runbook

_Include only if the project is hosted/deployed somewhere._

## Target
<Host, region, why chosen — see DECISIONS.>

## Prerequisites (accounts, DNS, tokens)
<Each third-party account, noted just-in-time on the ROADMAP row of the module that needs it.>

## Steps
1. <Provision>
2. <Install runtime>
3. <Deploy artifact>
4. <Ingress/TLS/auth>
5. <Secrets: how they reach the host without being committed (CI secrets + deploy-time env write)>

## Verify
<Health check command + expected output.>

## Rollback / teardown
