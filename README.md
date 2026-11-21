# Financial Medallion Lakehouse & Audit Anomaly Pipeline (Databricks)

End-to-end financial analytics and audit risk pipeline built on **Databricks (Unity Catalog, Delta Lake, PySpark, Spark SQL, AI/BI Dashboards)** using a synthetic multi-currency General Ledger dataset (~5,100 records).

## Architecture (Medallion Pattern)

```mermaid
flowchart LR
    A[Raw CSVs in UC Volume] --> B[Bronze Delta Tables\nRaw + Lineage Metadata]
    B --> C[Silver Clean Delta\nDedup, FX Norm, Z-Score]
    B --> Q[Silver Quarantine Delta\nCorrupt & Unmapped Rows]
    C --> D[Gold KPI Tables\nP&L, Budget Variance, Audit Risks]
    D --> E[Databricks AI/BI Dashboard]
