# AWX Automatización Azure - Escalado de App Service Plans# AWX Automatización Sencilla



Automatización profesional con AWX para gestión inteligente de costos en Azure mediante escalado automático de App Service Plans según horario.Este repositorio contiene playbooks de ejemplo para demostrar el uso básico de AWX, incluyendo automatización de descubrimiento de recursos Azure.



## 🎯 Funcionalidad Principal## Playbooks incluidos:



**Escalado Automático por Horario:**### 🔧 Playbooks básicos:

- ⬆️ **08:00 - 18:00 (Lunes-Viernes)**: Escala a **Basic (B1)** para rendimiento completo- **sistema_info.yml** - Recopila información del sistema

- ⬇️ **18:00 - 08:00 + Fines de semana**: Reduce a **Free (F1)** para ahorrar costos- **sistema_info_simple.yml** - Versión simplificada y robusta

- 💰 **Ahorro estimado**: ~$13/mes por App Service Plan- **ping_test.yml** - Test simple de conectividad

- **servidor_remoto.yml** - Automatización para servidores remotos

## 📋 Playbooks Disponibles

### ☁️ Playbooks Azure:

### Automatización por Horario- **azure_dynamic_inventory.yml** - Descubrimiento automático de recursos Azure

- **`azure_auto_scale_by_time.yml`** - Escalado automático inteligente por horario- **azure_discovery_demo.yml** - Simulación de descubrimiento (sin credenciales)



### Control Manual## Funcionalidades Azure:

- **`azure_list_service_plans.yml`** - Lista todos los App Service Plans

- **`azure_scale_up_to_basic.yml`** - Escala manualmente a Basic (B1)### 🔍 Descubrimiento automático de recursos:

- **`azure_scale_down_to_free.yml`** - Reduce manualmente a Free (F1)- Resource Groups

- Virtual Machines

### Playbooks Básicos- Storage Accounts

- **`sistema_info.yml`** - Información del sistema- Virtual Networks

- **`ping_test.yml`** - Test de conectividad- App Services

- **`servidor_remoto.yml`** - Automatización para servidores remotos- SQL Servers

- AKS Clusters

## 🔐 Configuración en AWX

### 📋 Generación de inventarios dinámicos:

### 1. Crear Credenciales Azure- Agrupación por Resource Group

- Agrupación por ubicación/región

Ve a **AWX → Credentials → Add**:- Agrupación por tamaño de VM

- **Name**: `Azure Service Principal`- Agrupación por estado (running/stopped)

- **Credential Type**: `Microsoft Azure Resource Manager`

- Completa con las credenciales del Service Principal creado## Configuración en AWX:



### 2. Crear Inventario### Para Azure (con credenciales):

1. Crear credenciales tipo "Microsoft Azure Resource Manager"

Ve a **AWX → Inventories → Add**:2. Usar playbook `azure_dynamic_inventory.yml`

- **Name**: `Azure Localhost`3. Programar ejecución periódica

- Añade host: `localhost` con `ansible_connection: local`

### Para demo (sin credenciales):

### 3. Crear Job Templates1. Usar playbook `azure_discovery_demo.yml`

2. Ver inventario simulado generado

#### Template 1: Escalado Automático

- **Name**: `Azure Auto Scale by Time`## Archivos generados:

- **Job Type**: `Run`- `/tmp/azure_inventory_[timestamp].yml` - Inventario dinámico

- **Inventory**: `Azure Localhost`- `/tmp/azure_resources_report_[timestamp].json` - Reporte completo

- **Project**: `Automatizaciones`- `/tmp/azure_simulated_inventory_[timestamp].ini` - Inventario demo

- **Playbook**: `playbooks/azure_auto_scale_by_time.yml`

- **Credentials**: `Azure Service Principal`## Automatización periódica:

Configura un Schedule en AWX para ejecutar automáticamente cada hora/día y mantener el inventario actualizado.
### 4. Programar Ejecución Automática

Ve a **Schedules → Add**:

**Schedule 1: Scale UP (Inicio jornada)**
- **Name**: `Scale UP - Start Work Day`
- **Frequency**: `Diaria - 08:00 UTC (Lunes-Viernes)`

**Schedule 2: Scale DOWN (Fin jornada)**
- **Name**: `Scale DOWN - End Work Day`
- **Frequency**: `Diaria - 18:00 UTC (Lunes-Viernes)`

## 💡 Ventajas

- ✅ **~62% de ahorro** en costos de App Service
- ⚡ **Rendimiento completo** en horario laboral
- 🌙 **Modo económico** automático fuera de horario
- 📊 **Reportes detallados** de cada ejecución
- 🔄 **100% automatizado** sin intervención manual

## 🛠️ Modificar Horarios

Edita `playbooks/azure_auto_scale_by_time.yml`:

```yaml
vars:
  business_hours_start: 8   # Hora inicio (UTC)
  business_hours_end: 18    # Hora fin (UTC)
  working_days: [1, 2, 3, 4, 5]  # 1=Lun, 7=Dom
```