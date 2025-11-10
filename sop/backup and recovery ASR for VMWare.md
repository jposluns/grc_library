# Standard Operating Procedure: Backup and Recovery – Azure Site Recovery (ASR) for VMware Production Systems

## Document Control

| Version | Date | Author | Change History |
|----------|------|---------|----------------|
| 0.1 |  |  | Initial Draft |

---

## Approval

| Role | Name | Approval Date |
|-------|------|---------------|
| Director of IT Service Delivery |  |  |
| Chief Information Officer (CIO) |  |  |
| Chief Information Security Officer (CISO) |  |  |
| Chief Security Officer (CSO-Physical) |  |  |
| Chief Risk Officer (CRO) |  |  |

---

## Purpose

To define the process for replication, backup, and recovery of production VMware workloads using **Microsoft Azure Site Recovery (ASR)**, including point-in-time recovery for SQL databases.  

This SOP ensures consistent protection of critical business systems and alignment with resilience and business-continuity objectives under ISO 22301, ISO 27031, COBIT DSS04, and NIST SP 800-34r1.

---

## Scope

This SOP applies to all **production virtual machines** running on **VMware vSphere** identified as critical business systems. It covers ASR configuration, replication, monitoring, and restoration procedures, including SQL database point-in-time recovery.

---

## 1. Responsibilities

| Role | Responsibility |
|------|----------------|
| **IT Operations Manager** | Ensures ASR policies are maintained, tested, and periodically reviewed for effectiveness. |
| **Infrastructure Engineer** | Configures and monitors ASR replication, validates synchronization, and performs failovers or test failovers as required. |
| **Database Administrator (DBA)** | Manages SQL backups, transaction log schedules, and executes point-in-time restores during recovery events. |
| **Service Desk** | Records and escalates outage notifications, anomalies, or restore requests following the incident-management process. |

---

## 2. Replication and Backup Requirements

| Item | Requirement |
|------|--------------|
| **Environment** | VMware vSphere (Production) |
| **Replication Target** | Microsoft Azure Site Recovery |
| **Replication Frequency** | 15 minutes (**RPO ≤ 15 minutes**) |
| **Recovery Location** | Azure Recovery Services Vault / Secondary Azure Region (if applicable) |
| **SQL Backup Strategy** | Full daily backup + transaction log backups to support point-in-time restore |
| **Testing Frequency** | Quarterly non-disruptive failover test |
| **Retention Policy** | In accordance with the Data Retention and Recovery Standard |

---

## 3. Azure Site Recovery Configuration Overview

1. Install the **Azure Site Recovery Mobility Service** on each protected virtual machine.  
2. Deploy and register the **VMware ASR Configuration Server** with Azure.  
3. Assign VMs to a **Replication Policy** configured for a 15-minute Recovery Point Objective (RPO).  
4. Verify that replicated disks are stored in **Azure managed disks** (Standard or Premium based on performance requirements).  
5. Map ASR networking to the appropriate **Azure Virtual Network and Subnet** for failover.  
6. Enable **Boot Order Groups** for dependent application stacks (for example: SQL before application servers).  
7. Confirm replication health daily and document metrics per the Backup and Recovery Register.

---

## 4. SQL Point-in-Time Recovery Configuration

1. Configure SQL backups using one of the approved methods:  
   - SQL Server Managed Backup to URL (Azure Storage)  
   - SQL Server Agent Full + Differential + Log backup schedule  
   - Azure Backup for SQL in VM  
2. Set **Transaction Log Backup Frequency** to support the required recovery window.  
3. Monitor SQL backup job success daily via monitoring dashboard or job alerts.  
4. Retain backups per the **Data Retention Policy** (for example, 14 days, 30 days, or 6 months).  
5. Validate restore tests at least quarterly and document results in the **Recovery Test Register**.

---

## 5. Failover Procedure (Disaster Recovery Event)

1. Confirm disaster declaration through IT leadership per the **Incident Response and Recovery Plan**.  
2. Open the **Azure Portal** and navigate to the appropriate **Recovery Services Vault**.  
3. Select the affected VM(s) and choose **Failover**.  
4. Select **Latest Recovery Point** unless an earlier point is required to preserve data integrity.  
5. Initiate failover and monitor VM provisioning in Azure.  
6. After VMs are running:  
   - Update DNS records and routing as required.  
   - Validate firewall and network rules.  
   - Confirm application service integrity and user access.  
7. Record the event, recovery point used, and restoration time in the **Disaster Recovery Log**.

---

## 6. SQL Point-in-Time Restore Procedure

1. Identify the required restore timestamp and corresponding transaction logs.  
2. In SQL Server Management Studio, connect to the SQL instance in the failover environment.  
3. Restore the most recent full backup.  
4. Apply differential backups if applicable.  
5. Apply transaction log backups up to the desired point-in-time.  
6. Validate database integrity (`DBCC CHECKDB`) and confirm application connectivity.  
7. Document the restore procedure and verification results in the **Backup and Recovery Register**.

---

## 7. Test Failover Procedure (Quarterly)

1. Launch **Test Failover** in Azure Site Recovery (do not select standard failover).  
2. Use an **isolated test network** to avoid production conflicts.  
3. Validate the following:  
   - Virtual machine boot order  
   - Application login and service functionality  
   - Database integrity and replication status  
4. Document results, identified issues, and remediation actions.  
5. Shut down the test environment and complete test failover cleanup.  
6. Update the **Disaster Recovery Test Report** and review outcomes with IT Operations and Risk Management.

---

## 8. Monitoring and Reporting

- Monitor ASR replication health daily and record exceptions.  
- Review alerting thresholds monthly to ensure visibility of degraded RPO/RTO metrics.  
- Provide quarterly ASR compliance and test reports to the **Enterprise Risk Committee (ERC)**.  
- Ensure key performance indicators (KPI) and metrics align with the **Digital Trust Performance Framework**.

---

## 9. References and Framework Alignment

- **ISO 22301:2019** Business Continuity Management Systems  
- **ISO 27031:2011** ICT Readiness for Business Continuity  
- **ISO 27001 / 27002:2022** Information Security Controls  
- **COBIT 2025 DSS04 / DSS05** Manage Continuity and Security Services  
- **NIST SP 800-34r1** Contingency Planning Guide for Federal Information Systems  
- **Cloud Security Alliance (CSA) CCM v5** – BCR (Business Continuity and Resilience) and AIS (Application and Interface Security) domains  
- **Azure Site Recovery and Azure Backup Documentation**  
- **Data Retention and Recovery Standard**  
- **Incident Response and Recovery Plan**  

---

## Definitions

Refer to the **Role Authority Register** for definitions of organizational roles and authorities.

---

**End of Document**
