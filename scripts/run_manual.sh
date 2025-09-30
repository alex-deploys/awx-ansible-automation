#!/bin/bash
#
# Script de ejemplo para ejecutar el playbook manualmente
# (fuera de AWX para pruebas)
#

# Configurar variables de Azure
export AZURE_SUBSCRIPTION_ID="tu-subscription-id-aqui"
export AZURE_TENANT="tu-tenant-id-aqui" 
export AZURE_CLIENT_ID="tu-client-id-aqui"
export AZURE_SECRET="tu-client-secret-aqui"

# Directorio del proyecto
PROJECT_DIR="/home/alazar/acciona/ansible-automatizaciones"

# Instalar dependencias (solo la primera vez)
echo "Instalando dependencias de Ansible..."
ansible-galaxy collection install -r "$PROJECT_DIR/requirements.yml"

# Ejecutar el playbook
echo "Ejecutando playbook de escalado automático..."
ansible-playbook \
  -i "$PROJECT_DIR/inventory/hosts" \
  "$PROJECT_DIR/playbooks/azure_serviceplan_autoscaler.yml" \
  -e "azure_subscription_id=$AZURE_SUBSCRIPTION_ID" \
  -e "azure_tenant_id=$AZURE_TENANT" \
  -e "azure_client_id=$AZURE_CLIENT_ID" \
  -e "azure_client_secret=$AZURE_SECRET" \
  -v

echo "Ejecución completada. Consulta el log en /tmp/azure_serviceplan_autoscaler.log"