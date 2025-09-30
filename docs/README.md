# Azure Service Plan Auto Scaler

Este proyecto contiene un playbook de Ansible para AWX que automatiza el escalado de Azure Service Plans basándose en horarios laborales.

## 📋 Descripción

El playbook busca todos los Azure Service Plans que tengan el tag `schedule:8x5` y realiza escalado automático:

- **Horario laboral** (8:00-17:00, Lunes-Viernes): Scale UP a **B1**
- **Horario no laboral** (noches, fines de semana): Scale DOWN a **F1**

## 🏗️ Estructura del Proyecto

```
ansible-automatizaciones/
├── playbooks/
│   └── azure_serviceplan_autoscaler.yml    # Playbook principal
├── inventory/
│   └── hosts                               # Inventario para localhost
├── templates/
│   └── azure_vars_template.yml             # Template de variables
└── docs/
    └── README.md                           # Esta documentación
```

## 🚀 Configuración en AWX

### 1. Prerequisitos

- AWX/Ansible Tower instalado y configurado
- Colección `azure.azcollection` instalada
- Service Principal de Azure con permisos para gestionar Service Plans

### 2. Credenciales de Azure

Crea una credencial personalizada en AWX con los siguientes campos:

```yaml
azure_subscription_id: "tu-subscription-id"
azure_tenant_id: "tu-tenant-id"  
azure_client_id: "tu-client-id"
azure_client_secret: "tu-client-secret"
```

### 3. Configuración del Job Template

1. **Nombre**: `Azure Service Plan Auto Scaler`
2. **Tipo de trabajo**: `Run`
3. **Inventario**: Usar el inventario local incluido
4. **Proyecto**: Apuntar a este repositorio
5. **Playbook**: `playbooks/azure_serviceplan_autoscaler.yml`
6. **Credenciales**: Seleccionar la credencial de Azure creada

### 4. Variables Extra (Opcional)

Puedes sobrescribir la configuración por defecto usando extra_vars:

```yaml
work_hours:
  start: 9
  end: 18
  timezone: "Europe/Madrid"

scaling_config:
  work_hours_sku: "S1"
  off_hours_sku: "F1"
```

## 🏷️ Etiquetado de Service Plans

Para que un Service Plan sea gestionado por este sistema, debe tener el tag:

```
schedule: 8x5
```

### Ejemplo de etiquetado con Azure CLI:

```bash
az appservice plan update \
  --resource-group mi-resource-group \
  --name mi-service-plan \
  --set tags.schedule=8x5
```

### Ejemplo de etiquetado con Terraform:

```hcl
resource "azurerm_service_plan" "example" {
  name                = "mi-service-plan"
  resource_group_name = "mi-resource-group"
  location           = "West Europe"
  os_type            = "Linux"
  sku_name           = "B1"

  tags = {
    schedule = "8x5"
  }
}
```

## ⏰ Programación en AWX

### Escalado Automático

Configura un **Schedule** en AWX para ejecutar el playbook automáticamente:

1. Ve a **Templates** → **Schedules**
2. Crea un nuevo schedule:
   - **Nombre**: `Auto Scale Service Plans`
   - **Tipo**: `Run`
   - **Cron**: `0 */2 * * *` (cada 2 horas)
   - **Zona horaria**: `Europe/Madrid`

### Horarios Recomendados

- **Cada 2 horas**: `0 */2 * * *`
- **Al inicio y fin del día laboral**: `0 7,18 * * 1-5`
- **Cada hora en días laborales**: `0 * * * 1-5`

## 📊 Logging y Monitoreo

El playbook genera logs en `/tmp/azure_serviceplan_autoscaler.log` con información de cada ejecución:

```
2024-10-01T10:00:00Z - Escalado automático ejecutado: 5 planes encontrados, 3 escalados a B1 (horario laboral)
2024-10-01T19:00:00Z - Escalado automático ejecutado: 5 planes encontrados, 3 escalados a F1 (horario no laboral)
```

## 🔧 Personalización

### Modificar Horarios Laborales

Edita las variables en el playbook o usa extra_vars:

```yaml
work_hours:
  start: 9      # 9:00 AM
  end: 18       # 6:00 PM
  timezone: "Europe/Madrid"
```

### Modificar SKUs de Escalado

```yaml
scaling_config:
  work_hours_sku: "S1"    # SKU más potente para horario laboral
  off_hours_sku: "F1"    # SKU económico para horario no laboral
```

### Usar Diferentes Tags

```yaml
scaling_config:
  target_tag: "autoscale:enabled"  # Buscar otro tag
```

## 🧪 Modo de Prueba

Para probar sin realizar cambios reales, añade la variable:

```yaml
dry_run: true
```

## ⚠️ Consideraciones Importantes

1. **Permisos**: El Service Principal necesita permisos de `Contributor` en los Resource Groups
2. **Zonas horarias**: Asegúrate de configurar la zona horaria correcta
3. **Costos**: F1 es gratuito pero tiene limitaciones; B1 tiene costo por hora
4. **Downtime**: El escalado puede causar breves interrupciones en las aplicaciones
5. **Dependencies**: Algunas aplicaciones pueden tener dependencias específicas de SKU

## 🆘 Solución de Problemas

### Error de Autenticación

```
FAILED - RETRYING: authentication failed
```

**Solución**: Verificar las credenciales de Azure y permisos del Service Principal.

### No se Encuentran Service Plans

**Solución**: Verificar que los Service Plans tengan el tag `schedule:8x5` configurado.

### Error de Permisos

```
The client does not have authorization to perform action
```

**Solución**: Asignar el rol `Contributor` al Service Principal en el Resource Group.

## 📝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.