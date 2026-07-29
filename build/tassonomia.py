#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La tassonomia ufficiale AZ-104 e la mappa da cui ci allineiamo.

Fonte: study guide ufficiale, skills measured al 17 aprile 2026.
https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-104

Perché sta in un file suo: `sotto_argomento` non è un'etichetta libera, è la
chiave con cui il simulatore dice "ripassa questo" e con cui si misura la
copertura. Se lo stesso obiettivo compare con due nomi, le categorie da
ripassare si spezzano in due e le percentuali mentono. Qui c'è l'elenco chiuso,
e chi aggiunge domande ci si attacca.
"""

# I 82 obiettivi ufficiali, nell'ordine della study guide, per dominio.
UFFICIALI = {
    "Manage Azure identities and governance": [
        # Manage Microsoft Entra users and groups
        "Create users and groups",
        "Manage user and group properties",
        "Manage licenses in Microsoft Entra ID",
        "Manage external users",
        "Configure self-service password reset (SSPR)",
        # Manage access to Azure resources
        "Manage built-in Azure roles",
        "Assign roles at different scopes",
        "Interpret access assignments",
        # Manage Azure subscriptions and governance
        "Implement and manage Azure Policy",
        "Configure resource locks",
        "Apply and manage tags on resources",
        "Manage resource groups",
        "Manage subscriptions",
        "Manage costs by using alerts, budgets, and Azure Advisor recommendations",
        "Configure management groups",
    ],
    "Implement and manage storage": [
        # Configure access to storage
        "Configure Azure Storage firewalls and virtual networks",
        "Create and use shared access signature (SAS) tokens",
        "Configure stored access policies",
        "Manage access keys",
        "Configure identity-based access for Azure Files",
        # Configure and manage storage accounts
        "Create and configure storage accounts",
        "Configure Azure Storage redundancy",
        "Configure object replication",
        "Configure storage account encryption",
        "Manage data by using Azure Storage Explorer and AzCopy",
        # Configure Azure Files and Azure Blob Storage
        "Create and configure a file share in Azure Files",
        "Create and configure a container in Azure Blob Storage",
        "Configure storage tiers",
        "Configure soft delete for blobs and containers",
        "Configure snapshots and soft delete for Azure Files",
        "Configure blob lifecycle management",
        "Configure blob versioning",
    ],
    "Deploy and manage Azure compute resources": [
        # ARM templates / Bicep
        "Interpret an Azure Resource Manager template or a Bicep file",
        "Modify an existing Azure Resource Manager template",
        "Modify an existing Bicep file",
        "Deploy resources by using an Azure Resource Manager template or a Bicep file",
        "Export a deployment as an Azure Resource Manager template or convert an "
        "Azure Resource Manager template to a Bicep file",
        # Create and configure virtual machines
        "Create a virtual machine",
        "Configure encryption at host for Azure virtual machines",
        "Move a virtual machine to another resource group, subscription, or region",
        "Manage virtual machine sizes",
        "Manage virtual machine disks",
        "Deploy virtual machines to availability zones and availability sets",
        "Deploy and configure an Azure Virtual Machine Scale Sets",
        # Containers
        "Create and manage an Azure Container Registry",
        "Provision a container by using Azure Container Instances",
        "Provision a container by using Azure Container Apps",
        "Manage sizing and scaling for containers, including Azure Container "
        "Instances and Azure Container Apps",
        # App Service
        "Provision an App Service plan",
        "Configure scaling for an App Service plan",
        "Create an App Service",
        "Configure certificates and Transport Layer Security (TLS) for an App Service",
        "Map an existing custom DNS name to an App Service",
        "Configure backup for an App Service",
        "Configure networking settings for an App Service",
        "Configure deployment slots for an App Service",
    ],
    "Implement and manage virtual networking": [
        # Configure and manage virtual networks
        "Create and configure virtual networks and subnets",
        "Create and configure virtual network peering",
        "Configure public IP addresses",
        "Configure user-defined routes",
        "Troubleshoot network connectivity",
        # Configure secure access
        "Create and configure network security groups (NSGs) and application security groups",
        "Evaluate effective security rules in NSGs",
        "Implement Azure Bastion",
        "Configure service endpoints for Azure platform as a service (PaaS)",
        "Configure private endpoints for Azure PaaS",
        # Name resolution and load balancing
        "Configure Azure DNS",
        "Configure an internal or public load balancer",
        "Troubleshoot load balancing",
    ],
    "Monitor and maintain Azure resources": [
        # Monitor resources
        "Interpret metrics in Azure Monitor",
        "Configure log settings in Azure Monitor",
        "Query and analyze logs in Azure Monitor",
        "Set up alert rules, action groups, and alert processing rules in Azure Monitor",
        "Configure and interpret monitoring of virtual machines, storage accounts, "
        "and networks by using Azure Monitor Insights",
        "Use Azure Network Watcher and Connection monitor",
        # Backup and recovery
        "Create a Recovery Services vault",
        "Create an Azure Backup vault",
        "Create and configure a backup policy",
        "Perform backup and restore operations by using Azure Backup",
        "Configure Azure Site Recovery for Azure resources",
        "Perform a failover to a secondary region by using Site Recovery",
        "Configure and interpret reports and alerts for backups",
    ],
}

TUTTI = [s for lista in UFFICIALI.values() for s in lista]

# Etichette usate in banca -> obiettivo ufficiale.
# A sinistra ci sono varianti di nome, sinonimi e un obiettivo ritirato.
RINOMINA = {
    # --- identità e governance ---
    # Riscritture in forma ufficiale
    "Provide access to Azure resources by assigning roles at different scopes":
        "Assign roles at different scopes",
    "Configure cost management":
        "Manage costs by using alerts, budgets, and Azure Advisor recommendations",
    # Ciclo di vita di utenti e gruppi: erano tre etichette per un obiettivo solo.
    # Le domande sotto queste due parlano di eliminazione e ripristino, che è
    # gestione del ciclo di vita, non delle proprietà.
    "Create, configure, and manage users": "Create users and groups",
    "Create, configure, and manage groups": "Create users and groups",
    # I ruoli custom non sono un obiettivo a sé nella study guide: la sezione
    # "Manage access to Azure resources" li assorbe qui, ed è dove uno li cerca.
    "Create custom role-based access control (RBAC) roles, including Azure roles "
    "and Microsoft Entra roles": "Manage built-in Azure roles",
    "Create custom role definitions": "Manage built-in Azure roles",

    # --- storage ---
    "Create and configure a container": "Create and configure a container in Azure Blob Storage",

    # --- compute ---
    "Interpret an ARM template or Bicep file":
        "Interpret an Azure Resource Manager template or a Bicep file",
    "Modify an existing ARM template": "Modify an existing Azure Resource Manager template",
    "Deploy a resource by using an ARM template or Bicep file":
        "Deploy resources by using an Azure Resource Manager template or a Bicep file",
    "Deploy and configure an Azure Virtual Machine Scale Set":
        "Deploy and configure an Azure Virtual Machine Scale Sets",
    "Create and manage an Azure container registry": "Create and manage an Azure Container Registry",
    "Provision a container using Azure Container Instances":
        "Provision a container by using Azure Container Instances",
    "Provision a container using Azure Container Apps":
        "Provision a container by using Azure Container Apps",
    "Configure deployment slots": "Configure deployment slots for an App Service",
    # Obiettivo RITIRATO il 17 aprile 2026, sostituito da encryption at host.
    # Le domande sotto questa etichetta parlano già di encryption at host: era
    # l'etichetta a essere rimasta indietro, non il contenuto.
    "Configure Azure Disk Encryption": "Configure encryption at host for Azure virtual machines",

    # --- rete ---
    "Configure user-defined network routes": "Configure user-defined routes",
    "Create and configure network security groups (NSGs) and application security groups (ASGs)":
        "Create and configure network security groups (NSGs) and application security groups",
    "Configure service endpoints for PaaS":
        "Configure service endpoints for Azure platform as a service (PaaS)",
    "Configure private endpoints for PaaS": "Configure private endpoints for Azure PaaS",

    # --- monitoraggio ---
    "Perform a failover to a secondary region":
        "Perform a failover to a secondary region by using Site Recovery",
}


def normalizza(sotto_argomento):
    """Riporta un'etichetta alla forma ufficiale. Idempotente."""
    return RINOMINA.get(sotto_argomento, sotto_argomento)


def dominio_di(sotto_argomento):
    for dom, lista in UFFICIALI.items():
        if sotto_argomento in lista:
            return dom
    return None
