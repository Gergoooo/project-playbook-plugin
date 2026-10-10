---
id: 06-churn-ml-pipeline
tier: full
repos: 1
expect: [data_model,attributions,features]
---
A machine-learning pipeline that predicts customer churn from a subscription company's usage logs: ingestion, feature engineering, model training with experiment tracking, a nightly batch scoring job, and a dashboard for the retention team. Small data team of three, data lives in Snowflake, must not leak PII.
