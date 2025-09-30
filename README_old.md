# AWX Automatización Sencilla

Este repositorio contiene playbooks de ejemplo para demostrar el uso básico de AWX, incluyendo automatización de descubrimiento de recursos Azure.

## Playbooks incluidos:

### 🔧 Playbooks básicos:
- **sistema_info.yml** - Recopila información del sistema
- **sistema_info_simple.yml** - Versión simplificada y robusta
- **ping_test.yml** - Test simple de conectividad
- **servidor_remoto.yml** - Automatización para servidores remotos

### ☁️ Playbooks Azure:
- **azure_dynamic_inventory.yml** - Descubrimiento automático de recursos Azure
- **azure_discovery_demo.yml** - Simulación de descubrimiento (sin credenciales)

## Funcionalidades Azure:

### 🔍 Descubrimiento automático de recursos:
- Resource Groups
- Virtual Machines
- Storage Accounts
- Virtual Networks
- App Services
- SQL Servers
- AKS Clusters

### 📋 Generación de inventarios dinámicos:
- Agrupación por Resource Group
- Agrupación por ubicación/región
- Agrupación por tamaño de VM
- Agrupación por estado (running/stopped)

## Configuración en AWX:

### Para Azure (con credenciales):
1. Crear credenciales tipo "Microsoft Azure Resource Manager"
2. Usar playbook `azure_dynamic_inventory.yml`
3. Programar ejecución periódica

### Para demo (sin credenciales):
1. Usar playbook `azure_discovery_demo.yml`
2. Ver inventario simulado generado

## Archivos generados:
- `/tmp/azure_inventory_[timestamp].yml` - Inventario dinámico
- `/tmp/azure_resources_report_[timestamp].json` - Reporte completo
- `/tmp/azure_simulated_inventory_[timestamp].ini` - Inventario demo

## Automatización periódica:
Configura un Schedule en AWX para ejecutar automáticamente cada hora/día y mantener el inventario actualizado.