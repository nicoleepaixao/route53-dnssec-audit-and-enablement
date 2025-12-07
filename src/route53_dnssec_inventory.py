#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Route53 DNSSEC Inventory Script (Sanitized Version)
---------------------------------------------------

This script performs a complete DNSSEC audit across multiple AWS accounts.

- Read-only operations (STS, Route53, Route53Domains)
- Identifies public/private hosted zones
- Detects DNSSEC status for each zone
- Checks if domains are registered in Route53 Domains
- Outputs results in CSV format

No changes are made to DNS, hosted zones, or KMS keys.
"""

import boto3
import botocore
import csv
import os


# Example profiles (sanitized)
AWS_PROFILES = [
    "prod",
    "staging",
    "dev",
    "qa",
    "network"
]


def get_account_id(session):
    """Returns AWS Account ID for the profile."""
    try:
        sts = session.client("sts")
        resp = sts.get_caller_identity()
        return resp.get("Account", "UNKNOWN")
    except Exception:
        return "UNKNOWN"


def get_registered_domains(session):
    """Retrieves Route53 registered domains."""
    try:
        client = session.client("route53domains", region_name="us-east-1")
    except Exception:
        return set(), False

    domains = set()
    marker = None

    while True:
        try:
            resp = client.list_domains(Marker=marker) if marker else client.list_domains()
        except Exception:
            return domains, False

        for d in resp.get("Domains", []):
            name = d.get("DomainName", "").rstrip(".")
            if name:
                domains.add(name)

        marker = resp.get("NextPageMarker")
        if not marker:
            break

    return domains, True


def get_dnssec_status(route53_client, hosted_zone_id):
    """Returns the DNSSEC status for a public hosted zone."""
    try:
        resp = route53_client.get_dnssec(HostedZoneId=hosted_zone_id)
        status_block = resp.get("Status", {})
        return status_block.get("Status", "UNKNOWN")
    except route53_client.exceptions.DNSSECNotFound:
        return "NOT_CONFIGURED"
    except Exception:
        return "UNKNOWN"


def inventory_profile(profile_name):
    """Audits DNSSEC status for one AWS profile."""
    print(f"\n=== Profile: {profile_name} ===")

    try:
        session = boto3.Session(profile_name=profile_name)
    except botocore.exceptions.ProfileNotFound:
        print(f"[ERROR] Profile not found: {profile_name}")
        return []

    account_id = get_account_id(session)
    route53 = session.client("route53")

    registered_domains, registrar_read_ok = get_registered_domains(session)

    results = []

    paginator = route53.get_paginator("list_hosted_zones")
    for page in paginator.paginate():
        for hz in page.get("HostedZones", []):
            hz_id = hz["Id"].split("/")[-1]
            domain_name = hz["Name"].rstrip(".")

            config = hz.get("Config", {})
            private_zone = config.get("PrivateZone", False)

            if private_zone:
                dnssec_status = "NOT_SUPPORTED_PRIVATE_ZONE"
            else:
                dnssec_status = get_dnssec_status(route53, hz_id)

            registered = (
                "YES" if domain_name in registered_domains else "NO"
                if registrar_read_ok else "UNKNOWN"
            )

            results.append(
                {
                    "profile": profile_name,
                    "account_id": account_id,
                    "hosted_zone_id": hz_id,
                    "domain_name": domain_name,
                    "zone_type": "PRIVATE" if private_zone else "PUBLIC",
                    "registered_in_route53": registered,
                    "dnssec_status": dnssec_status,
                }
            )

            print(
                f" - {domain_name} ({'PRIVATE' if private_zone else 'PUBLIC'}) "
                f"Registrar={registered}, DNSSEC={dnssec_status}"
            )

    return results


def main():
    os.makedirs("../output", exist_ok=True)

    all_rows = []

    for profile in AWS_PROFILES:
        all_rows.extend(inventory_profile(profile))

    output_file = "../output/route53_dnssec_inventory.csv"
    fieldnames = [
        "profile",
        "account_id",
        "hosted_zone_id",
        "domain_name",
        "zone_type",
        "registered_in_route53",
        "dnssec_status",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

    print(f"\nInventory completed successfully.")
    print(f"CSV saved at: {output_file}")


if __name__ == "__main__":
    main()
