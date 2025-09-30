# ⚠️ Limitaciones de AWX Execution Environment

## Problema

El contenedor de AWX no incluye todos los SDKs de Azure por defecto. Algunos módulos de `azure.azcollection` requieren librerías Python adicionales que no están instaladas:

### Módulos que NO funcionan en AWX por defecto:
- ❌ `azure_rm_sqlserver_info` - Requiere `azure-mgmt-sql`
- ❌ `azure_rm_postgresqlflexibleserver_info` - Requiere `azure-mgmt-postgresqlflexibleservers`
- ❌ `azure_rm_mysqlflexibleserver_info` - Requiere `azure-mgmt-rdbms`
- ❌ Algunos módulos avanzados de red, DNS, etc.

### Error típico:
```
ModuleNotFoundError: No module named 'azure.mgmt.postgresqlflexibleservers'
fatal: [localhost]: FAILED! => {"msg": "Failed to import the required Python library..."}
```

## ✅ Solución

Usa el playbook **simplificado** que solo utiliza módulos básicos disponibles en AWX:

### Playbooks AWX-Compatible:

| Playbook | Propósito | AWX | Local |
|----------|-----------|-----|-------|
| `azure_simple_inventory.yml` | Inventario simplificado (solo App Service Plans) | ✅ | ✅ |
| `azure_auto_scale_by_time.yml` | Escalado automático F1↔B1 | ✅ | ✅ |
| `azure_list_service_plans.yml` | Listar App Service Plans | ✅ | ✅ |
| `azure_scale_up_to_basic.yml` | Escalar a B1 manualmente | ✅ | ✅ |
| `azure_scale_down_to_free.yml` | Escalar a F1 manualmente | ✅ | ✅ |
| `awx_diagnostics.yml` | Diagnóstico de entorno | ✅ | ✅ |

### Playbooks SOLO para uso local:

| Playbook | Propósito | Requiere |
|----------|-----------|----------|
| `azure_update_dynamic_inventory.yml` | Inventario completo (VMs, SQL, etc.) | SDKs completos de Azure |

## 🔧 Configuración en AWX

### Opción 1: Usar Playbooks Simplificados (Recomendado)

**Ventajas:**
- ✅ Funciona inmediatamente sin configuración extra
- ✅ Suficiente para automatización de App Service Plans
- ✅ Más rápido y ligero

**Configuración:**
```yaml
# Job Template
Name: Azure - Update Dynamic Inventory
Playbook: playbooks/azure_simple_inventory.yml  # ← Usar este
```

### Opción 2: Custom Execution Environment (Avanzado)

Si necesitas TODOS los módulos de Azure, debes crear una imagen Docker personalizada:

#### 2.1. Crear archivo `execution-environment.yml`:

```yaml
---
version: 3

images:
  base_image:
    name: quay.io/ansible/awx-ee:latest

dependencies:
  python_interpreter:
    package_system: python311
  
  python:
    - azure-cli-core>=2.40.0
    - azure-common>=1.1.28
    - azure-mgmt-compute>=30.0.0
    - azure-mgmt-network>=25.0.0
    - azure-mgmt-resource>=23.0.0
    - azure-mgmt-web>=7.0.0
    - azure-mgmt-storage>=21.0.0
    - azure-mgmt-sql>=4.0.0
    - azure-mgmt-rdbms>=10.1.0
    - azure-mgmt-postgresqlflexibleservers>=1.0.0
    - msrest>=0.7.1
    - msrestazure>=0.6.4
  
  galaxy:
    collections:
      - name: azure.azcollection
        version: ">=2.0.0"
      - name: community.general
        version: ">=5.0.0"

options:
  package_manager_path: /usr/bin/microdnf
```

#### 2.2. Construir la imagen:

```bash
# Instalar ansible-builder
pip install ansible-builder

# Construir la imagen
ansible-builder build \
  --tag custom-awx-ee:azure-complete \
  --container-runtime podman

# Subir a registry (opcional)
podman push custom-awx-ee:azure-complete your-registry.com/custom-awx-ee:azure-complete
```

#### 2.3. Configurar en AWX:

1. Ve a **Administration → Execution Environments**
2. Click **Add**
3. Configura:
   - **Name**: `Custom Azure Complete`
   - **Image**: `custom-awx-ee:azure-complete` (o tu registry)
4. **Save**

5. En tus **Job Templates**, selecciona:
   - **Execution Environment**: `Custom Azure Complete`

## 🎯 Recomendación

Para tu caso de uso (automatización de App Service Plans):

✅ **Usa los playbooks simplificados** - Son suficientes y funcionan de inmediato.

❌ **No necesitas** un execution environment custom - Solo si planeas automatizar SQL, PostgreSQL, MySQL, etc.

## 📊 Comparación

### Playbook Simplificado (azure_simple_inventory.yml)
```
Descubre:
✅ Resource Groups
✅ App Service Plans (Free, Basic, Standard, Premium)
✅ Web Apps
✅ Storage Accounts (opcional)
✅ Virtual Machines (opcional)

Agrupa por:
✅ Tipo de recurso
✅ SKU Tier (Free, Basic, Standard)
✅ Resource Group
✅ Ubicación

Tiempo: ~10-15 segundos
Requiere: Solo azure.azcollection (ya incluido en AWX)
```

### Playbook Completo (azure_update_dynamic_inventory.yml)
```
Descubre TODO:
✅ Todo lo anterior +
✅ SQL Servers
✅ PostgreSQL Flexible Servers
✅ MySQL Flexible Servers
✅ Virtual Networks
✅ Public IPs
✅ Y más...

Tiempo: ~30-60 segundos
Requiere: SDKs completos de Azure (custom EE)
```

## 🧪 Probar Antes de Configurar

Ejecuta el playbook de diagnóstico para ver qué está disponible:

```yaml
# En AWX, crear Job Template:
Name: AWX Diagnostics
Playbook: playbooks/awx_diagnostics.yml
Credentials: Azure - Service Principal

# Launch y revisa el output
```

El diagnóstico te mostrará:
- ✅ Qué módulos Python de Azure están instalados
- ✅ Si puedes conectar a Azure
- ✅ Qué módulos de ansible funcionan
- ✅ Variables de entorno configuradas

## 📚 Referencias

- [AWX Execution Environments](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html)
- [Ansible Builder](https://ansible-builder.readthedocs.io/)
- [Azure Collection](https://galaxy.ansible.com/ui/repo/published/azure/azcollection/)

---

**💡 TL;DR**: Usa `azure_simple_inventory.yml` en AWX - funciona perfectamente para tu automatización de App Service Plans.
