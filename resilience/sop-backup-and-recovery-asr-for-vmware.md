# Standard Operating Procedure: Backup and Recovery – Azure Site Recovery (ASR) for VMware Production Systems

## Metadata

| Field | Details |
|-------|----------|
| **Document Title** | Backup and Recovery Standard Operating Procedure (Azure Site Recovery – VMware Production Systems) |
| **Document Type** | Standard Operating Procedure (SOP) |
| **Version** | 0.1 |
| **Date** |  |
| **Document Owner** | Director of IT |
| **Approving Authority** | Chief Information Officer (CIO) |
| **Related Documents** | Data Retention and Recovery Standard; Incident Response and Recovery Plan; IT Operations Documentation Framework; Digital Trust Performance Framework |
| **Classification** | Controlled – Internal Use |
| **Category** | IT Operations / Business Continuity |
| **Review Frequency** | Annual or following major infrastructure change |
| **Repository Path** | /resilience/sop-backup-and-recovery-asr-for-vmware.md |
| **Confidentiality** | **None (Public Domain, CC0 License)** |

---

## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |

---

## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Director of IT |  |  |
| Chief Information Officer (CIO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Chief Security Officer (CSO-Physical) |  |  |
| Chief Risk Officer (CRO) |  |  |

---

## Purpose

To define the process for replication, backup, validation, and recovery of production VMware workloads using Microsoft Azure Site Recovery (ASR), including point-in-time SQL database recovery.  

This SOP ensures that business-critical systems are resilient, recoverable, and tested according to enterprise continuity requirements and applicable standards (ISO 22301, ISO 27031, COBIT DSS04, NIST SP 800-34r1, and CSA CCM v5 BCR).

---

## Scope

This SOP applies to all production virtual machines running on VMware vSphere that are identified as critical business systems.  
It covers Azure Site Recovery (ASR) configuration, replication, monitoring, and restoration procedures, including SQL database point-in-time recovery.  
It also defines ongoing testing, documentation, and compliance verification to ensure disaster-readiness.

---

## 1. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **Director of IT** | Owns the ASR policy, coordinates periodic reviews, ensures compliance with retention and resilience standards, and validates recovery KPIs. |
| **Infrastructure Engineer** | Configures ASR replication policies, maintains health monitoring, performs planned and emergency failovers, and coordinates with cloud teams. |
| **Database Administrator (DBA)** | Configures, manages, and validates SQL backups, ensures correct log-backup frequency, and performs point-in-time restores. |
| **Service Desk** | Logs all incidents, triggers escalation to IT and Infrastructure during an outage or restore request, and maintains communication with end users. |
| **Director of IT Service Delivery** | Provides oversight, ensures quarterly testing, and validates audit documentation for compliance and assurance reviews. |

---

## 2. Replication and Backup Requirements

| Item | Requirement |
|------|--------------|
| **Environment** | VMware vSphere (Production) |
| **Replication Target** | Microsoft Azure Site Recovery Vault |
| **Replication Frequency** | Every 15 minutes (**RPO ≤ 15 minutes**) |
| **Recovery Location** | Primary Azure Recovery Services Vault or secondary Azure region |
| **SQL Backup Strategy** | Full daily backup + transaction log backups to support point-in-time restore |
| **Testing Frequency** | Quarterly non-disruptive failover test |
| **Retention Policy** | Per Data Retention and Recovery Standard (minimum 30 days for SQL, 7 years for audit records) |

---

## 3. Azure Site Recovery Configuration Overview

1. Install **Azure Site Recovery Mobility Service** on each protected VM.  
2. Deploy and register the **VMware ASR Configuration Server** and connect it to Azure.  
3. Assign VMs to a **Replication Policy** configured for an RPO of 15 minutes or less.  
4. Verify that replicated disks are stored in **Azure Managed Disks** (Standard or Premium).  
5. Map **failover networking** to the appropriate Azure VNet/Subnet and verify routing.  
6. Configure **Boot Order Groups** for application tiers (e.g., SQL before Application).  
7. Monitor **replication health daily**; resolve alerts within one business day.  
8. Maintain a **Replication Checklist** documenting each VM’s replication state, last RPO timestamp, and validation date.  
9. Ensure **encryption at rest and in transit** is enabled.  
10. Archive configuration exports monthly for audit traceability.

---

## 4. SQL Point-in-Time Recovery Configuration

1. Use one of the following approved methods:  
   - SQL Server Managed Backup to URL (Azure Blob Storage)  
   - SQL Server Agent Full + Differential + Log schedule  
   - Azure Backup for SQL in VM  
2. Set **Transaction Log Backup Frequency** (default 15 minutes) to align with RPO.  
3. Validate SQL backup job success daily using automated reports.  
4. Retain backups per the Data Retention Policy (standard 30 days, critical systems 6 months).  
5. Perform and document **quarterly restore tests** validating point-in-time capability.  
6. Use **RA-GZRS storage** for redundancy and geographic durability.  
7. Document restore paths, storage accounts, and encryption keys in the Backup Inventory Register.

---

## 5. Failover Procedure (Disaster Recovery Event)

1. **Incident Confirmation**  
   - The **Director of IT** confirms a disaster declaration and activates the Incident Response and Recovery Plan.  
2. **Preparation for Failover**  
   - Validate replication health and latest recovery point.  
3. **Initiate Failover**  
   - In the Azure Portal → Recovery Services Vault → Replicated Items → Select VM → **Failover** → **Latest Recovery Point**.  
   - Start failover and monitor provisioning.  
4. **Post-Failover Validation**  
   - Validate boot sequence, networking, and DNS updates.  
   - Confirm application and database integrity.  
   - Verify user access and security baselines.  
5. **Documentation**  
   - Record recovery point, event ID, and total recovery time in the Disaster Recovery Log.  
   - Submit a post-incident report to the CIO and Enterprise Risk Committee within five business days.

---

## 6. SQL Point-in-Time Restore Procedure

1. Identify the target restore timestamp.  
2. Connect to the SQL instance in the failover environment.  
3. Restore the latest full backup with NORECOVERY.  
4. Apply differential backups if used.  
5. Sequentially apply transaction log backups with STOPAT = `<timestamp>`.  
6. Complete recovery with RECOVERY, run `DBCC CHECKDB`, and confirm service connectivity.  
7. Record procedure, timestamp, and validation outcome in the Backup and Recovery Register.

---

## 7. Test Failover Procedure (Quarterly)

1. Launch **Test Failover** (do not use standard failover).  
2. Use an **isolated test network**.  
3. Validate:  
   - VM boot order.  
   - Application and database login functionality.  
   - SQL integrity checks.  
   - Achievement of RPO/RTO objectives.  
4. Record results, remediation actions, and completion in the Test Report.  
5. Perform cleanup of test resources.  
6. Submit report to IT and Risk Management for review.

---

## 8. Monitoring and Reporting

- Review ASR replication health daily and remediate exceptions within one business day.  
- Validate Azure Monitor and Log Analytics integration for protected VMs.  
- Produce weekly RPO/RTO status summaries.  
- Conduct monthly trend reviews to identify anomalies.  
- Provide quarterly performance reports to the **Enterprise Risk Committee (ERC)** and **CIO**.  
- Maintain dashboards and evidence in the **Digital Trust Performance Framework** workspace.

---

## 9. Post-Event Review and Continuous Improvement

- Conduct a Post-Implementation Review within ten business days of any failover or test.  
- Identify lessons learned, update ASR configurations, and modify documentation.  
- Log all improvement actions in the **Continuous Improvement Register**.  
- Deliver an annual resilience and recovery training workshop for infrastructure and DBA teams.

---

## 10. Compliance and Framework Alignment

| Framework | Relevant Sections | Compliance Objective |
|------------|------------------|----------------------|
| **ISO 22301:2019** | Clauses 8–10 | Ensure business continuity through tested procedures. |
| **ISO 27031:2011** | Clause 7 | Define structured ICT readiness for continuity. |
| **ISO 27001 / 27002:2022** | Annex A.5, A.7, A.12, A.17 | Maintain information security and backup resilience. |
| **COBIT 2025** | DSS04, DSS05 | Manage continuity, availability, and security services. |
| **NIST SP 800-34r1** | Chapters 2–5 | Define contingency and recovery processes. |
| **CSA CCM v5** | BCR, AIS | Cloud and application resilience controls. |
| **Trade and Supply Chain Programs** | WCO SAFE, ISO 28000, PIP, CTPAT, AEO | Physical security and continuity compliance alignment. |

---

## Definitions

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.

---

**End of Document**
