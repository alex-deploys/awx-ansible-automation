# 🎯 Guía Rápida: Configuración del Inventario Dinámico en AWX

## ✅ Lo que hemos completado

1. ✅ **Playbook de Inventario Dinámico** (`azure_update_dynamic_inventory.yml`)
   - Descubre automáticamente todos los recursos Azure
   - Genera inventarios en formatos YAML, INI y JSON
   - Organiza recursos por tipo, tier, resource group y ubicación

2. ✅ **Script de Inventario** (`azure_dynamic_inventory.py`)
   - Compatible con AWX/Ansible Tower
   - Formato JSON estándar de inventario dinámico

3. ✅ **Configuraciones de Plugin**
   - `azure_rm.yml` - Para Virtual Machines
   - `azure_app_service_plans.yml` - Para App Service Plans

4. ✅ **Documentación completa** (`docs/INVENTARIO_DINAMICO.md`)

## 📋 Próximos pasos en AWX

### 1️⃣ Sincronizar Project en AWX

```bash
# Acceder a AWX
http://192.168.49.2:32741

# Login: admin / aIqwROq7sr4cncdc8gMGdtDMF1EpRn48
```

1. Ve a **Resources → Projects**
2. Encuentra `Ansible Automatizaciones`
3. Click en el botón **Sync** (🔄)
4. Espera a que termine (debería aparecer ✅)

### 2️⃣ Crear Credencial Azure

1. Ve a **Resources → Credentials**
2. Click **Add** (➕)
3. Configura:
   - **Name**: `Azure - Service Principal`
   - **Credential Type**: `Microsoft Azure Resource Manager`
   - **Subscription ID**: (de `.azure_credentials.yml`)
   - **Client ID**: (de `.azure_credentials.yml`)
   - **Client Secret**: (de `.azure_credentials.yml`)
   - **Tenant ID**: (de `.azure_credentials.yml`)
4. **Save**

### 3️⃣ Crear Inventario Dinámico

#### Opción A: Inventario Manual con Host Localhost

1. Ve a **Resources → Inventories**
2. Click **Add** → **Add inventory**
3. Configura:
   - **Name**: `Azure Dynamic Inventory`
   - **Organization**: Default
4. **Save**

5. Ve a la pestaña **Hosts**
6. Click **Add**
7. Configura:
   - **Name**: `localhost`
   - **Variables** (en formato YAML):
   ```yaml
   ansible_connection: local
   ansible_python_interpreter: /usr/bin/python3
   ```
8. **Save**

#### Opción B: Inventario con Source desde Proyecto (Avanzado)

1. Crea el inventario como arriba
2. Ve a la pestaña **Sources**
3. Click **Add**
4. Configura:
   - **Name**: `Azure Resource Discovery`
   - **Source**: `Sourced from a Project`
   - **Project**: `Ansible Automatizaciones`
   - **Inventory File**: `inventory/azure_dynamic_inventory.py`
   - **Credential**: `Azure - Service Principal`
   - **Update on Launch**: ✅
5. **Save**
6. Click **Sync** (🔄)

### 4️⃣ Crear Job Template para Actualizar Inventario

1. Ve a **Resources → Templates**
2. Click **Add** → **Add job template**
3. Configura:
   - **Name**: `Azure - Update Dynamic Inventory`
   - **Job Type**: Run
   - **Inventory**: `Azure Dynamic Inventory`
   - **Project**: `Ansible Automatizaciones`
   - **Playbook**: `playbooks/azure_update_dynamic_inventory.yml`
   - **Credentials**:
     - Type `Microsoft Azure Resource Manager` → `Azure - Service Principal`
   - **Options**:
     - ✅ Enable Concurrent Jobs: NO
4. **Save**

### 5️⃣ Probar el Inventario

1. Ve al Job Template `Azure - Update Dynamic Inventory`
2. Click **Launch** (🚀)
3. Observa la ejecución
4. Debería mostrar:
   ```
   📊 Recursos Descubiertos:
   📁 Resource Groups: X
   🖥️  Virtual Machines: X
   📱 App Service Plans: X
   ...
   ```

### 6️⃣ Crear Job Template para Escalado Automático

1. Ve a **Resources → Templates**
2. Click **Add** → **Add job template**
3. Configura:
   - **Name**: `Azure - Auto Scale Service Plans by Time`
   - **Job Type**: Run
   - **Inventory**: `Azure Dynamic Inventory`
   - **Project**: `Ansible Automatizaciones`
   - **Playbook**: `playbooks/azure_auto_scale_by_time.yml`
   - **Credentials**:
     - Type `Microsoft Azure Resource Manager` → `Azure - Service Principal`
4. **Save**

### 7️⃣ Configurar Schedule para Ejecución Automática

#### Schedule 1: Verificación cada hora

1. En el Job Template `Azure - Auto Scale Service Plans by Time`
2. Pestaña **Schedules**
3. Click **Add**
4. Configura:
   - **Name**: `Check and Scale - Every Hour`
   - **Repeat Frequency**: Every `1` Hour
   - **Start Date/Time**: Ahora
   - **Time Zone**: Europe/Madrid
5. **Save**

#### Schedule 2: Actualizar inventario cada 30 minutos

1. En el Job Template `Azure - Update Dynamic Inventory`
2. Pestaña **Schedules**
3. Click **Add**
4. Configura:
   - **Name**: `Update Inventory - Every 30 min`
   - **Repeat Frequency**: Every `30` Minutes
   - **Start Date/Time**: Ahora
   - **Time Zone**: Europe/Madrid
5. **Save**

## 🎯 Resultado Final

Una vez configurado, tendrás:

✅ **Inventario dinámico** que se actualiza automáticamente cada 30 minutos
✅ **Escalado automático** de App Service Plans cada hora:
   - 🕗 8:00 AM - 6:00 PM (Lunes-Viernes) → **B1 (Basic)**
   - 🌙 6:00 PM - 8:00 AM + Fines de semana → **F1 (Free)**
✅ **Ahorro de costos** optimizado
✅ **Recursos organizados** por tipo, tier, resource group, ubicación

## 📊 Grupos de Inventario Disponibles

Después de ejecutar el inventario dinámico, podrás usar estos grupos en tus playbooks:

| Grupo | Uso |
|-------|-----|
| `azure_app_service_plans` | Todos los App Service Plans |
| `tier_free` | Solo planes Free (F1) |
| `tier_basic` | Solo planes Basic (B1, B2, B3) |
| `tier_standard` | Solo planes Standard |
| `rg_<nombre>` | Por Resource Group |
| `location_<region>` | Por región |

## 🔍 Verificar que Funciona

### Desde AWX:
1. **Dashboard** → Deberías ver los jobs programados
2. **Resources → Inventories → Azure Dynamic Inventory**
   - Deberías ver hosts después de ejecutar el update
3. **Views → Jobs**
   - Verifica que los schedules se ejecutan correctamente

### Desde CLI local (prueba):
```bash
cd /home/alazar/acciona/ansible-automatizaciones

# Probar inventario
ansible-playbook playbooks/azure_update_dynamic_inventory.yml \
  --extra-vars "@.azure_credentials.yml"

# Ver inventario generado
cat /tmp/azure_dynamic_inventory.yml

# Probar escalado (simulación)
ansible-playbook playbooks/azure_auto_scale_by_time.yml \
  --extra-vars "@.azure_credentials.yml" \
  --check
```

## 🆘 Ayuda

- **Documentación completa**: `docs/INVENTARIO_DINAMICO.md`
- **Troubleshooting**: Ver sección de troubleshooting en la documentación
- **Logs de AWX**: 
  ```bash
  kubectl logs -n awx deployment/awx-demo-task -f
  ```

## 📝 Archivos Importantes

```
ansible-automatizaciones/
├── playbooks/
│   ├── azure_update_dynamic_inventory.yml  ← Actualiza inventario
│   ├── azure_auto_scale_by_time.yml        ← Escalado automático
│   ├── azure_list_service_plans.yml        ← Listar planes
│   └── test_dynamic_inventory.yml          ← Pruebas
├── inventory/
│   ├── azure_dynamic_inventory.py          ← Script para AWX
│   ├── azure_rm.yml                        ← Config VMs
│   └── azure_app_service_plans.yml         ← Config App Plans
├── docs/
│   └── INVENTARIO_DINAMICO.md              ← Documentación completa
└── .azure_credentials.yml                  ← Credenciales (LOCAL, no en git)
```

---

**¡Todo listo!** Sigue los pasos en orden y tendrás un sistema de automatización completo. 🚀
