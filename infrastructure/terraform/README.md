# Terraform Infrastructure - Salesgroup Toolbox

## Azure Configuration

### Subscription Details
- **Subscription Name:** sg_tool_resources
- **Subscription ID:** `3c88104d-250c-4d63-b126-1bba4ccc1ec5`
- **Tenant:** Salesgroup Stockholm AB
- **Tenant ID:** `1aa70fb4-db14-442b-a980-dd9b6c2175fc`
- **Primary Region:** swedencentral (Stockholm)

### Service Principal
- **Name:** sp-sg_toolbox-terraform
- **App ID:** `a9f06a53-e80b-44f3-8377-2e0a24ad4a9f`
- **Purpose:** Terraform automation
- **Permissions:** Contributor role on subscription

---

## Backend Configuration

### State Storage
- **Storage Account:** sgtoolboxtf
- **Resource Group:** rg-terraform-state
- **Container:** tfstate
- **Location:** swedencentral

### State Files
- **QA Environment:** `qa-toolbox.tfstate`
- **Prod Environment:** `prod-toolbox.tfstate`

**Note:** We use separate backend configurations per environment for better isolation and security.

---

## Project Structure

```
infrastructure/terraform/
├── main.tf                      # Provider config + resources
├── variables.tf                 # Input variable definitions
├── outputs.tf                   # Output values
├── backend.tf                   # Backend configuration (base)
├── environments/
│   ├── qa.tfvars               # QA environment values
│   ├── qa.backend.hcl          # QA state file configuration
│   ├── prod.tfvars             # Prod environment values
│   └── prod.backend.hcl        # Prod state file configuration
└── README.md                    # This file
```

## Naming standards according to Microsoft CAF 
<resurstyp>-<applikation>-<workload/instans>-<env>
vm-toolbox-web-01-qa
vm-toolbox-db-01-qa
aks-toolbox-qa
psql-toolbox-qa
```

---

## Environments

### QA (Test/Staging)
- **Purpose:** Testing and validation before production
- **Resource Naming:** `<resource>-toolbox-qa`
- **Example RG:** `rg-toolbox-qa`
- **State File:** `qa-toolbox.tfstate`

### Production
- **Purpose:** Live environment for end users
- **Resource Naming:** `<resource>-toolbox-prod`
- **Example RG:** `rg-toolbox-prod`
- **State File:** `prod-toolbox.tfstate`

---

## Setup Instructions

### Prerequisites
1. **Azure CLI:** `az --version >= 2.53`
2. **Terraform:** `terraform --version >= 1.6.0`
3. **Environment Variables:** `.env` file with:
   ```bash
   export ARM_CLIENT_ID="a9f06a53-e80b-44f3-8377-2e0a24ad4a9f"
   export ARM_CLIENT_SECRET="<service-principal-password>"
   export ARM_TENANT_ID="1aa70fb4-db14-442b-a980-dd9b6c2175fc"
   export ARM_SUBSCRIPTION_ID="3c88104d-250c-4d63-b126-1bba4ccc1ec5"
   ```

### First Time Setup

1. **Load environment variables:**
   ```bash
   cd infrastructure/terraform
   source ../../.env
   ```

2. **Initialize Terraform (QA):**
   ```bash
   terraform init -reconfigure -backend-config=environments/qa.backend.hcl
   ```

3. **Validate configuration:**
   ```bash
   terraform validate
   terraform fmt
   ```

4. **Plan changes:**
   ```bash
   terraform plan -var-file=environments/qa.tfvars
   ```

5. **Apply changes:**
   ```bash
   terraform apply -var-file=environments/qa.tfvars
   ```

---

## Daily Workflow

### Working with QA Environment

```bash
# 1. Load credentials
source ../../.env

# 2. Ensure correct backend
terraform init -reconfigure -backend-config=environments/qa.backend.hcl

# 3. Make changes to .tf files

# 4. Format and validate
terraform fmt
terraform validate

# 5. Preview changes
terraform plan -var-file=environments/qa.tfvars

# 6. Apply changes
terraform apply -var-file=environments/qa.tfvars
```

### Switching to Production

```bash
# 1. Re-initialize with prod backend
terraform init -reconfigure -backend-config=environments/prod.backend.hcl

# 2. Plan for production
terraform plan -var-file=environments/prod.tfvars

# 3. Review carefully, then apply
terraform apply -var-file=environments/prod.tfvars
```

---

## Important Commands

### State Management
```bash
# List all resources
terraform state list

# Show specific resource details
terraform state show azurerm_resource_group.toolbox

# Refresh state from Azure
terraform refresh -var-file=environments/qa.tfvars
```

### Outputs
```bash
# Show all outputs
terraform output

# Show specific output
terraform output resource_group_name
```

### Cleanup
```bash
# Destroy all resources (QA)
terraform destroy -var-file=environments/qa.tfvars

# Destroy specific resource
terraform destroy -target=azurerm_resource_group.toolbox -var-file=environments/qa.tfvars
```

---

## Resources Managed by Terraform

### Current Infrastructure (QA)
- ✅ Resource Group: `rg-toolbox-qa`
- ✅ Container Registry: `sgtoolboxacrqa`
- 🔄 PostgreSQL: (coming next)
- 🔄 Key Vault: (coming next)
- 🔄 Container Apps: (coming next)

### Future Infrastructure (Prod)
- ⏳ Resource Group: `rg-toolbox-prod`
- ⏳ Container Registry: `sgtoolboxacrprod`
- ⏳ PostgreSQL: (TBD)
- ⏳ Key Vault: (TBD)
- ⏳ Container Apps: (TBD)

---

## Troubleshooting

### Common Issues

**"Backend initialization required"**
```bash
terraform init -reconfigure -backend-config=environments/qa.backend.hcl
```

**"Error acquiring state lock"**
- Wait for other operations to complete
- Or force unlock (use with caution):
  ```bash
  terraform force-unlock <LOCK_ID>
  ```

**"Reference to undeclared resource"**
- Check spelling of resource names in main.tf
- Ensure resource exists before referencing it

**"Provider version constraint not met"**
```bash
terraform init -upgrade
```

---

## Security Notes

### Secrets Management
- ❌ **NEVER** commit `.env` file to git
- ❌ **NEVER** commit `.tfvars` files with secrets
- ✅ Use Azure Key Vault for application secrets
- ✅ Use Service Principal for Terraform authentication
- ✅ Rotate Service Principal password regularly

### State File Security
- ✅ State files stored in Azure Storage (encrypted at rest)
- ✅ Access controlled via RBAC
- ✅ State locking enabled (prevents concurrent modifications)
- ✅ Separate state files per environment

---

## Best Practices

1. **Always load .env before running terraform:**
   ```bash
   source ../../.env && terraform plan -var-file=environments/qa.tfvars
   ```

2. **Always specify var-file explicitly:**
   - Prevents accidental deployments to wrong environment

3. **Run plan before apply:**
   - Review changes carefully, especially for production

4. **Use version control:**
   - Commit all `.tf` files
   - Commit `.terraform.lock.hcl` (locks provider versions)
   - DO NOT commit `.env` or state files

5. **Tag all resources:**
   - All resources have Environment, Project, and ManagedBy tags
   - Helps with cost tracking and resource management

---

## Cost Estimation

### QA Environment (Monthly)
- Resource Group: Free
- Container Registry (Basic): ~$5
- PostgreSQL (Burstable B1ms): ~$17
- Container Apps (2.5 vCPU, 198h/month): ~$25
- Key Vault (Standard): ~$0.50
- **Total:** ~$48/month

### Production Environment (Monthly)
- Estimated: ~$80-100/month (higher resources)

---

## Maintenance

### Regular Tasks
- [ ] Review and rotate Service Principal password (quarterly)
- [ ] Review resource costs (monthly)
- [ ] Update provider versions (as needed)
- [ ] Backup state files (automated via Azure Storage)
- [ ] Review access permissions (quarterly)

### Provider Updates
```bash
# Check for updates
terraform init -upgrade

# Lock to new version
git add .terraform.lock.hcl
git commit -m "Update Terraform providers"
```

---



## Support & Documentation

### Azure Provider Documentation
- [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Container Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/container_registry)
- [PostgreSQL Flexible Server](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_flexible_server)
- [Container Apps](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/container_app)

### Terraform Documentation
- [Terraform CLI](https://developer.hashicorp.com/terraform/cli)
- [Backend Configuration](https://developer.hashicorp.com/terraform/language/settings/backends/azurerm)
- [State Management](https://developer.hashicorp.com/terraform/language/state)

---

## Change Log

### 2025-10-16
- ✅ Initial setup completed
- ✅ Backend configured with separate state files
- ✅ QA and Prod environments defined
- ✅ Resource Group and Container Registry configured

---


**Maintained by:** Salesgroup Development Team  
**Last Updated:** 2025-10-16  
**Terraform Version:** >= 1.6.0  
**Azure Provider Version:** ~> 4.0