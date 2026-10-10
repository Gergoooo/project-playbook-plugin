---
id: 08-aws-terraform-infra
tier: full
repos: 1
expect: [deployment,ci]
---
Infrastructure-as-code for a startup's AWS setup: three environments (dev/staging/prod), VPC, ECS services, RDS Postgres, S3, CloudFront, IAM roles, secrets management and a CI pipeline that runs plan on PRs and apply on merge. Team of four, strict cost and security requirements.
