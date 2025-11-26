## Rotate Toolbox secrets - change plan

### change secret plan
#### Flow - All secrets except postgres
1. create new secrest in lastpass (or passowrd manager of choice)
2. set new secrets (se below)
3. !!Conatinerapp specifics!!- remove admin_user from sg_users table (wil be recreated on build) in porsgres
4. Trigger actions workflow to redeploy
5. test application


#### Things to note!!!!!!!!
- Webb app (conaitner app) only creates user if does not exists, old password will be actine unless remoce from sg_users table (postgres stauteful )
- posgrest: Make sure you have a backup admin pass word IF posgress password change goes wrong.
- Terraform will read new value in keyvault, and destroy old. sol be awar log will show change

#### Set key-vault secret
```bash
az keyvault secret set \
  --vault-name kv-toolbox-qa-v2 \
  --name openai-api-key \
  --value "nytt-hemligt-värde"

az keyvault secret set \
  --vault-name kv-toolbox-qa-v2 \
  --name flask-secret-key \
  --value "nytt-hemligt-värde"


#OBS! Admin andävändaren skapas bara OM den inte finns, om lösenordet skall roteras, måste det bytas manuellt!
az keyvault secret set \
  --vault-name kv-toolbox-qa-v2 \
  --name admin-password \
  --value "nytt-hemligt-värde"
```



## Postgres 
### Flow
1. Skapa bakupanvändare
2. Verifera rättigheter
2. Testa byta eget lösen på backup
3. testa byta toolbox admin lösen från backup
4. Om 3. = O, commit + quit
5. 

### Postgres commands
#### Connect (use cli locally or )
```bash
 -- 0. Connect to psql 
 psql "host=<endpoint-string>.postgres.database.azure.com port=5432 dbname=postgres user=toolboxadmin sslmode=require"
 psql "host=psql-toolbox-qa.postgres.database.azure.com port=5432 dbname=postgres user=toolboxadmin sslmode=require"
 psql "host=psql-toolbox-qa.postgres.database.azure.com port=5432 dbname=sg_toolbox user=toolboxadmin sslmode=require"
```

#### Steg 1. Skapa bakupanvändare och sätt rättigheter
```bash
  -- 1. Skapa backup admin INNAN du byter
CREATE USER toolboxadmin_backup WITH PASSWORD 'backup-password-123';
GRANT ALL PRIVILEGES ON DATABASE sg_toolbox TO toolboxadmin_backup;


ALTER USER toolboxadmin_backup WITH CREATEROLE CREATEDB BYPASSRLS;

ALTER USER toolboxadmin_backup WITH CREATEROLE CREATEDB BYPASSRLS;
GRANT ALL PRIVILEGES ON DATABASE sg_toolbox TO toolboxadmin_backup;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO toolboxadmin_backup;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO toolboxadmin_backup;
GRANT toolboxadmin TO toolboxadmin_backup WITH ADMIN OPTION;
```

#### check priviligens
```bash
SELECT 
    grantee, 
    table_schema, 
    table_name, 
    privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'toolboxadmin_backup'
ORDER BY table_name;
```

#### visa roller
```bash
SELECT 
    r.rolname as role,
    m.rolname as member_of
FROM pg_roles r
LEFT JOIN pg_auth_members am ON r.oid = am.member
LEFT JOIN pg_roles m ON am.roleid = m.oid
WHERE r.rolname IN ('toolboxadmin', 'toolboxadmin_backup');
```

#### Ändra lösenorder (förslagsvis från backupkontot för att verifiera rättigheter.)
-- 2. Nu kan du säkert ändra toolboxadmin
ALTER USER toolboxadmin PASSWORD 'nytt-losenord';



-- 3. Om något går fel, byt till backup i Key Vault

#### Clean up
-- 4. När allt fungerar, ta bort backup-användaren
```bash
Steg 1: Ta bort rättigheter
sql-- Ta bort databas-rättigheter
REVOKE ALL PRIVILEGES ON DATABASE sg_toolbox FROM toolboxadmin_backup;

-- Ta bort tabell-rättigheter
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM toolboxadmin_backup;

-- Ta bort sequence-rättigheter
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM toolboxadmin_backup;

Steg 2: Ta bort rollmedlemskap
sqlREVOKE toolboxadmin FROM toolboxadmin_backup;

Steg 3: Nu kan du droppa användaren
sqlDROP USER toolboxadmin_backup;
```bash
DROP USER toolboxadmin_backup;
```

### Change password in Key Vault 
#### Postgres admin password
az keyvault secret set \
  --vault-name kv-toolbox-qa-v2 \
  --name postgres-admin-password \
  --value "nytt-hemligt-värde"

#### Postgres connection string
```bash
az keyvault secret set \
  --vault-name kv-toolbox-qa-v2 \
  --name postgres-connection-string \
  --value "nytt-hemligt-värde"
```

- Toolbox specifix
```bash
az keyvault secret set \
  --vault-name kv-toolbox-qa-v2 \
  --name postgres-connection-string \
  --value "postgresql://toolboxadmin:DITT-NYA-LÖSENORD@psql-toolbox-qa.postgres.database.azure.com:5432/sg_toolbox?sslmode=require"
```

#### Deploy new version to get rid of cashed secrets
1. Run actiopons workflow
2. Manual deploy from CLI 
3. run copy in Azire cli 
az containerapp revision copy \
  --name ca-toolbox-web-qa \
  --resource-group rg-toolbox-qa

#### Check passwords
```bash
#check secret with azure cli 
az keyvault secret show \
  --vault-name kv-toolbox-qa-v2 \
  --name postgres-admin-password \
  --query "value" \
  --output tsv


  az keyvault secret show \
  --vault-name kv-toolbox-qa-v2 \
  --name postgres-connection-string \
  --query "value" \
  --output tsv
```