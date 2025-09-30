# 📋 Inventario Dinámico Azure para AWX

## 🎯 Descripción

Sistema de inventario dinámico que descubre automáticamente recursos de Azure y los organiza para su uso en AWX.

## 📦 Componentes

### 1. **Playbook de Actualización** (`azure_update_dynamic_inventory.yml`)
Descubre y cataloga todos los recursos Azure:
- ✅ Virtual Machines
- ✅ App Service Plans (Free, Basic, Standard)
- ✅ Web Apps
- ✅ Storage Accounts
- ✅ SQL Servers
- ✅ Virtual Networks

### 2. **Script de Inventario Dinámico** (`azure_dynamic_inventory.py`)
Script Python compatible con AWX para inventario dinámico en formato JSON.

### 3. **Configuraciones de Plugin** 
- `azure_rm.yml` - Inventario de VMs usando plugin nativo
- `azure_app_service_plans.yml` - Configuración específica para App Service Plans

### 4. **Formatos de Salida**
- **YAML**: `/tmp/azure_dynamic_inventory.yml` - Formato legible
- **INI**: `/tmp/azure_dynamic_inventory.ini` - Formato clásico Ansible
- **JSON**: `/tmp/azure_inventory_full_*.json` - Reporte completo con timestamp

## 🔧 Configuración en AWX

### Paso 1: Crear Credencial Azure

1. Ve a **Resources → Credentials**
2. Click en **Add** (➕)
3. Completa:
   - **Name**: `Azure - Service Principal`
   - **Organization**: Default
   - **Credential Type**: `Microsoft Azure Resource Manager`
   - **Subscription ID**: `<tu-subscription-id>`
   - **Client ID**: `<tu-client-id>`
   - **Client Secret**: `<tu-client-secret>`
   - **Tenant ID**: `<tu-tenant-id>`
4. Click **Save**

   > 💡 **Nota**: Usa las credenciales de tu Service Principal de Azure.  
   > Consulta `.azure_credentials.yml` (local, no en git) para los valores reales.

### Paso 2: Crear Project

1. Ve a **Resources → Projects**
2. Click en **Add** (➕)
3. Completa:
   - **Name**: `Ansible Automatizaciones`
   - **Organization**: Default
   - **Source Control Type**: `Git`
   - **Source Control URL**: `https://github.com/alex-deploys/awx-ansible-automation.git`
   - **Source Control Branch/Tag/Commit**: `main`
   - **Update Revision on Launch**: ✅ (marcado)
4. Click **Save**
5. Click en el botón **Sync** (🔄) para sincronizar

### Paso 3: Crear Inventario Dinámico

#### Opción A: Inventario con Actualización Automática (Recomendado)

1. Ve a **Resources → Inventories**
2. Click en **Add** → **Add inventory**
3. Completa:
   - **Name**: `Azure Dynamic Inventory`
   - **Organization**: Default
4. Click **Save**

5. Ve a la pestaña **Sources**
6. Click en **Add** (➕)
7. Completa:
   - **Name**: `Azure Resource Discovery`
   - **Source**: `Sourced from a Project`
   - **Project**: `Ansible Automatizaciones`
   - **Inventory File**: `inventory/azure_dynamic_inventory.py` o `inventory/azure_rm.yml`
   - **Credential**: `Azure - Service Principal`
   - **Update Options**:
     - ✅ Overwrite
     - ✅ Overwrite variables
     - ✅ Update on project update
   - **Update on Launch**: ✅
8. Click **Save**

9. **Sincronizar**: Click en el botón **Sync** (🔄)

#### Opción B: Inventario Manual con Playbook

1. Crear inventario básico con `localhost`
2. Ejecutar el playbook `azure_update_dynamic_inventory.yml` para generar archivos
3. Usar los archivos generados en `/tmp/` como inventario estático

### Paso 4: Crear Job Template para Actualizar Inventario

1. Ve a **Resources → Templates**
2. Click en **Add** → **Add job template**
3. Completa:
   - **Name**: `Azure - Update Dynamic Inventory`
   - **Job Type**: Run
   - **Inventory**: `Azure Dynamic Inventory`
   - **Project**: `Ansible Automatizaciones`
   - **Playbook**: `playbooks/azure_update_dynamic_inventory.yml`
   - **Credentials**: 
     - Type: `Microsoft Azure Resource Manager` → `Azure - Service Principal`
   - **Options**:
     - ✅ Enable Privilege Escalation: NO
     - ✅ Enable Concurrent Jobs: NO
4. Click **Save**

### Paso 5: Configurar Actualización Programada

1. En el Job Template creado, ve a la pestaña **Schedules**
2. Click en **Add** (➕)
3. Completa:
   - **Name**: `Update Inventory - Every 30 minutes`
   - **Start Date/Time**: Ahora
   - **Repeat Frequency**: Every `30` Minutes
   - **Time Zone**: Europe/Madrid
4. Click **Save**

## 🚀 Uso

### Probar Inventario Localmente

```bash
cd /home/alazar/acciona/ansible-automatizaciones

# Probar con credenciales locales
ansible-playbook playbooks/azure_update_dynamic_inventory.yml \
  --extra-vars "@.azure_credentials.yml"

# Ver inventario generado
cat /tmp/azure_dynamic_inventory.yml

# Probar inventario
ansible-playbook playbooks/test_dynamic_inventory.yml \
  --extra-vars "@.azure_credentials.yml"
```

### Usar en AWX

1. **Sincronizar Inventario**: 
   - Ve a **Resources → Inventories → Azure Dynamic Inventory**
   - Click en **Sources → Azure Resource Discovery**
   - Click **Sync** (🔄)

2. **Ver Recursos Descubiertos**:
   - Ve a **Resources → Inventories → Azure Dynamic Inventory → Hosts**
   - Deberías ver tus App Service Plans, VMs, etc.

3. **Usar en Job Templates**:
   - Selecciona `Azure Dynamic Inventory` como inventario
   - Los grupos disponibles serán:
     - `azure_app_service_plans` - Todos los App Service Plans
     - `tier_free` - Solo planes Free (F1)
     - `tier_basic` - Solo planes Basic (B1)
     - `tier_standard` - Solo planes Standard
     - `rg_<nombre>` - Por Resource Group
     - `location_<ubicacion>` - Por ubicación

## 📊 Grupos de Inventario Generados

| Grupo | Descripción | Ejemplo de Uso |
|-------|-------------|----------------|
| `azure_app_service_plans` | Todos los App Service Plans | Listar todos los planes |
| `tier_free` | Planes en tier Free (F1) | Identificar recursos gratuitos |
| `tier_basic` | Planes en tier Basic (B1, B2, B3) | Planes de bajo costo |
| `tier_standard` | Planes en tier Standard | Planes de producción |
| `rg_<nombre>` | Recursos por Resource Group | Agrupar por proyecto |
| `location_<region>` | Recursos por ubicación geográfica | Agrupar por región |
| `azure_vms` | Virtual Machines | Gestión de VMs |
| `azure_web_apps` | Web Apps y API Apps | Aplicaciones web |

## 🔄 Automatización con el Inventario

### Ejemplo: Escalar solo planes Free a Basic

```yaml
- name: Escalar planes Free a Basic
  hosts: tier_free  # ← Usa el grupo del inventario dinámico
  gather_facts: no
  tasks:
    - name: Escalar a B1
      azure.azcollection.azure_rm_appserviceplan:
        resource_group: "{{ azure_resource_group }}"
        name: "{{ inventory_hostname }}"
        sku:
          name: B1
          tier: Basic
```

### Ejemplo: Operación por Resource Group

```yaml
- name: Operación en Resource Group específico
  hosts: rg_DefaultResourceGroup-WEU  # ← Resource Group específico
  gather_facts: no
  tasks:
    - debug:
        msg: "Procesando {{ inventory_hostname }} en {{ azure_resource_group }}"
```

## 📝 Variables de Host Disponibles

Cada host en el inventario dinámico tiene estas variables:

### App Service Plans
- `ansible_host`: localhost (ya que son recursos cloud)
- `azure_resource_group`: Nombre del Resource Group
- `azure_location`: Ubicación (westeurope, etc.)
- `azure_sku_tier`: Tier del plan (Free, Basic, Standard)
- `azure_sku_name`: SKU específico (F1, B1, B2, etc.)
- `azure_sku_capacity`: Número de instancias
- `azure_resource_type`: Tipo de recurso
- `azure_plan_id`: ID completo del recurso en Azure

### Virtual Machines
- `ansible_host`: IP pública o privada
- `azure_resource_group`: Resource Group
- `azure_location`: Ubicación
- `azure_vm_size`: Tamaño de VM (Standard_D2s_v3, etc.)
- `azure_os_type`: Sistema operativo (Linux, Windows)
- `azure_resource_type`: virtual_machine

## 🎯 Próximos Pasos

1. ✅ **Configurar Credencial Azure** en AWX
2. ✅ **Crear Inventario Dinámico** con source desde proyecto
3. ✅ **Sincronizar** para descubrir recursos
4. ✅ **Verificar** que los hosts aparecen en el inventario
5. 🔄 **Crear Job Template** para escalado automático usando `tier_free` y `tier_basic`
6. 🔄 **Configurar Schedule** para ejecutar escalado según horario

## 🐛 Troubleshooting

### Problema: No aparecen recursos en el inventario

**Solución 1**: Verificar credenciales Azure
```bash
# Desde AWX, ejecutar playbook de test
ansible-playbook playbooks/azure_list_service_plans.yml
```

**Solución 2**: Verificar permisos del Service Principal
```bash
az role assignment list --assignee <tu-client-id> --all
```

**Solución 3**: Revisar logs de AWX
```bash
kubectl logs -n awx deployment/awx-demo-task -f
```

### Problema: Inventario no se actualiza

**Solución**: Forzar sincronización
1. Ve a **Resources → Inventories → Azure Dynamic Inventory**
2. Pestaña **Sources → Azure Resource Discovery**
3. Click en **Sync** (🔄)
4. Marca la opción **Overwrite** si es necesario

### Problema: Error de autenticación

**Solución**: Verificar que las credenciales en AWX coinciden con las de tu Service Principal:
- **Subscription ID**: `<tu-subscription-id>`
- **Client ID**: `<tu-client-id>`  
- **Tenant ID**: `<tu-tenant-id>`

> 💡 Consulta el archivo local `.azure_credentials.yml` para los valores correctos.

## 📚 Referencias

- [Azure RM Inventory Plugin](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/azure_rm_inventory.html)
- [AWX Dynamic Inventory](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html#add-source)
- [Ansible Azure Collection](https://galaxy.ansible.com/ui/repo/published/azure/azcollection/)
