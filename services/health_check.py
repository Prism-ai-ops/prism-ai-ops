import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config
from database.db import get_assets_by_application, save_health_result

# -------------------------------------------------
# SIMULATION FUNCTIONS
# -------------------------------------------------

def simulate_ping(asset):
    outcome = random.choices(['reachable', 'timeout'], weights=[85, 15])[0]
    status = 'PASS' if outcome == 'reachable' else 'FAIL'
    return {
        'asset_id': asset[0],
        'asset_name': asset[1],
        'check_type': 'ping',
        'status': status,
        'value': outcome
    }

def simulate_cpu(asset):
    value = random.randint(10, 98)
    if value < config.CPU_WARN:
        status = 'PASS'
    elif value < config.CPU_FAIL:
        status = 'WARN'
    else:
        status = 'FAIL'
    return {
        'asset_id': asset[0],
        'asset_name': asset[1],
        'check_type': 'cpu',
        'status': status,
        'value': f'{value}%'
    }

def simulate_memory(asset):
    value = random.randint(10, 98)
    if value < config.MEMORY_WARN:
        status = 'PASS'
    elif value < config.MEMORY_FAIL:
        status = 'WARN'
    else:
        status = 'FAIL'
    return {
        'asset_id': asset[0],
        'asset_name': asset[1],
        'check_type': 'memory',
        'status': status,
        'value': f'{value}%'
    }

def simulate_disk(asset):
    value = random.randint(10, 98)
    if value < config.DISK_WARN:
        status = 'PASS'
    elif value < config.DISK_FAIL:
        status = 'WARN'
    else:
        status = 'FAIL'
    return {
        'asset_id': asset[0],
        'asset_name': asset[1],
        'check_type': 'disk',
        'status': status,
        'value': f'{value}%'
    }

def simulate_service(asset):
    outcome = random.choices(['running', 'stopped'], weights=[90, 10])[0]
    status = 'PASS' if outcome == 'running' else 'FAIL'
    return {
        'asset_id': asset[0],
        'asset_name': asset[1],
        'check_type': 'service',
        'status': status,
        'value': outcome
    }

def simulate_port_check(asset):
    outcome = random.choices(['open', 'closed'], weights=[90, 10])[0]
    status = 'PASS' if outcome == 'open' else 'FAIL'
    return {
        'asset_id': asset[0],
        'asset_name': asset[1],
        'check_type': 'port_check',
        'status': status,
        'value': outcome
    }

# -------------------------------------------------
# ASSET TYPE ROUTING
# -------------------------------------------------

def run_asset_checks(asset):
    results = []
    asset_type = asset[2].lower()  # asset_type column

    # Ping runs for all asset types
    results.append(simulate_ping(asset))

    if asset_type in ['windows', 'linux']:
        results.append(simulate_cpu(asset))
        results.append(simulate_memory(asset))
        results.append(simulate_disk(asset))
        results.append(simulate_service(asset))

    elif asset_type in ['mssql', 'oracle']:
        results.append(simulate_disk(asset))
        results.append(simulate_service(asset))

    elif asset_type == 'network':
        results.append(simulate_port_check(asset))

    # Other: ping only

    return results

# -------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------

def run_health_checks(application_id):
    assets = get_assets_by_application(application_id)

    if not assets:
        return []

    all_results = []

    for asset in assets:
        results = run_asset_checks(asset)

        # Save each result to DB
        for r in results:
            save_health_result(
                asset_id=r['asset_id'],
                check_type=r['check_type'],
                status=r['status'],
                value=r['value']
            )

        all_results.extend(results)

    return all_results