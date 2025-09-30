#!/usr/bin/env python3
"""
Azure Dynamic Inventory Script para AWX
Genera inventario dinámico de recursos Azure en formato JSON

Uso:
  ./azure_dynamic_inventory.py --list
  ./azure_dynamic_inventory.py --host <hostname>
"""

import json
import sys
import argparse
import os
from datetime import datetime

def get_azure_inventory():
    """
    Genera inventario dinámico desde Azure
    En AWX, esto usará las credenciales configuradas automáticamente
    """
    
    # Estructura de inventario vacía
    inventory = {
        '_meta': {
            'hostvars': {}
        },
        'all': {
            'children': ['azure']
        },
        'azure': {
            'children': [
                'azure_app_service_plans',
                'azure_vms',
                'azure_web_apps',
                'tier_free',
                'tier_basic',
                'tier_standard'
            ],
            'vars': {
                'ansible_connection': 'local',
                'azure_managed': True,
                'inventory_updated': datetime.utcnow().isoformat()
            }
        },
        'azure_app_service_plans': {
            'hosts': [],
            'vars': {
                'azure_resource_type': 'app_service_plan'
            }
        },
        'azure_vms': {
            'hosts': [],
            'vars': {
                'azure_resource_type': 'virtual_machine'
            }
        },
        'azure_web_apps': {
            'hosts': [],
            'vars': {
                'azure_resource_type': 'web_app'
            }
        },
        'tier_free': {
            'hosts': [],
            'vars': {
                'azure_sku_tier': 'Free'
            }
        },
        'tier_basic': {
            'hosts': [],
            'vars': {
                'azure_sku_tier': 'Basic'
            }
        },
        'tier_standard': {
            'hosts': [],
            'vars': {
                'azure_sku_tier': 'Standard'
            }
        }
    }
    
    # Nota: En producción, aquí iría la lógica para consultar Azure usando SDK
    # AWX inyectará automáticamente las credenciales de Azure cuando se ejecute
    # Por ahora, devolvemos la estructura base que será poblada por el playbook
    
    return inventory

def get_host_vars(hostname):
    """
    Devuelve variables específicas de un host
    """
    # En AWX, esto se poblará automáticamente desde el inventario
    return {}

def main():
    parser = argparse.ArgumentParser(description='Azure Dynamic Inventory')
    parser.add_argument('--list', action='store_true', 
                       help='List all hosts')
    parser.add_argument('--host', action='store',
                       help='Get variables for a specific host')
    
    args = parser.parse_args()
    
    if args.list:
        inventory = get_azure_inventory()
        print(json.dumps(inventory, indent=2))
    elif args.host:
        hostvars = get_host_vars(args.host)
        print(json.dumps(hostvars, indent=2))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
