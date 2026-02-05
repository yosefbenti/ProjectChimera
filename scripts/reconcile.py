#!/usr/bin/env python3
"""Reconcile Delivery events and Payments samples.

Usage:
  python3 scripts/reconcile.py --delivery PATH --payments PATH --outdir out

If no paths provided the embedded sample data will be used.
"""
from io import StringIO
import argparse
import os
import pandas as pd

DELIVERY_SAMPLE = """
event_id	package_id	order_id	event_time	status	city
D2001	PK9001	O5001	2026-01-02 14:20	DELIVERED	Addis
D2002	PK9002	O5002	2026-01-03 16:10	DELIVERED	Addis
D2003	PK9003	O5003	2026-01-06 09:00	DELIVERED	Adama
D2004	PK9004	O5004	2026-01-06 18:30	DELIVERED	Addis
D2005	PK9005	O5005	2026-01-07 15:10	DELIVERED	BahirDar
D2006	PK9006	O5006	2026-02-01 10:05	DELIVERED	Addis
D2007	PK9007	O5007	2026-01-12 17:00	DELIVERED	Addis
D2008	PK9008	O5008	2026-01-15 13:45	DELIVERED	Addis
D2009	PK9009	O5009	2026-01-19 11:22	DELIVERED	Adama
D2010	PK9010	O5010	2026-01-20 16:00	DELIVERED	Addis
D2011	PK9011	O5011	2026-01-22 18:00	DELIVERED	Addis
D2012	PK9012	O5012	2026-01-23 15:40	DELIVERED	Hawassa
D2013	PK9013	O5013	2026-01-24 12:00	DELIVERED	Addis
D2014	PK9014	O5014	2026-01-26 09:10	DELIVERED	Addis
D2015	PK9015	O5015	2026-01-26 17:50	DELIVERED	Addis
D2016	PK9016	O5016	2026-01-29 14:10	FAILED	Addis
D2017	PK9017	O5017	2026-01-29 19:00	FAILED	Addis
D2018	PK9018	O5018	2026-02-02 11:00	DELIVERED	Addis
D2019	PK9019	O5019	2026-02-03 16:40	DELIVERED	Addis
D2020	PK9020	O5020	2026-01-31 15:00	RETURNED	Addis
D2021	PK9024	O5024	2026-01-13 12:00	DELIVERED	Addis (See <attachments>)
"""

PAYMENTS_SAMPLE = """
payment_id	order_id	package_id	customer_id	payment_date	amount	currency	payment_status	channel
P1001	O5001	PK9001	C101	2026-01-02	500	ETB	PAID	CARD
P1002	O5002	PK9002	C102	2026-01-03	700	ETB	PAID	MOBILE
P1003	O5003	PK9003	C103	2026-01-05	450	ETB	PAID	CARD
P1004	O5004	PK9004	C104	2026-01-06	600	ETB	PAID	CARD
P1005	O5005	PK9005	C105	2026-01-07	550	ETB	PAID	CASH
P1006	O5006	PK9006	C106	2026-01-10	800	ETB	PAID	CARD
P1007	O5007	PK9007	C107	2026-01-12	720	ETB	PAID	MOBILE
P1008	O5008	PK9008	C108	2026-01-15	300	ETB	PAID	CARD
P1009	O5009	PK9009	C109	2026-01-18	950	ETB	PAID	CARD
P1010	O5010	PK9010	C110	2026-01-20	400	ETB	PAID	CARD
P1011	O5011	PK9011	C111	2026-01-22	650	ETB	PAID	CARD
P1012	O5012	PK9012	C112	2026-01-23	480	ETB	PAID	MOBILE
P1013	O5013	PK9013	C113	2026-01-24	510	ETB	PAID	CARD
P1014	O5014	PK9014	C114	2026-01-25	530	ETB	PAID	CARD
P1015	O5015	PK9015	C115	2026-01-26	620	ETB	PAID	MOBILE
P1016	O5016	PK9016	C116	2026-01-28	770	ETB	PAID	CARD
P1017	O5017	PK9017	C117	2026-01-29	680	ETB	PAID	CARD
P1018	O5018	PK9018	C118	2026-01-30	390	ETB	PAID	MOBILE
P1019	O5019	PK9019	C119	2026-01-31	900	ETB	PAID	CARD
P1020	O5020	PK9020	C120	2026-01-31	460	ETB	PAID	CARD
P1021	O5006	PK9006	C106	2026-01-10	800	ETB	PAID	CARD
P1022	O5014	PK9014	C114	2026-01-25	530	ETB	PAID	CARD
P1023	O5021		C121	2026-01-29	500	ETB	PAID	CARD
P1024	O5022	PK9022	C122	2026-01-15	600	ETB	REFUNDED	CARD
P1025	O5023	PK9023	C123	2026-01-10	750	ETB	PAID	CARD
P1026	O5024	PK9024	C124	2026-01-12	1500	ETB	PAID	CARD (meta)
"""


def load_table(path: str, sample: str, parse_dates=None):
    """Load a table from path (auto-detect separators) or from the embedded sample.

    Returns a DataFrame with normalized column names (strip/lower).
    """
    if path:
        try:
            df = pd.read_csv(path, sep=None, engine='python', parse_dates=parse_dates)
        except Exception:
            # fall back to common separators
            for sep in [',', '\t', ';']:
                try:
                    df = pd.read_csv(path, sep=sep, engine='python', parse_dates=parse_dates)
                    break
                except Exception:
                    df = None
            if df is None:
                raise
    else:
        df = pd.read_csv(StringIO(sample), sep='\t', engine='python', parse_dates=parse_dates)

    # normalize column names
    df.columns = df.columns.astype(str).str.strip().str.lower()
    return df


def sanitize_delivery(df):
    # clean city trailing metadata
    if 'city' in df.columns:
        df['city'] = df['city'].astype(str).str.replace(r"\s*\(.*\)$", '', regex=True).str.strip()
    # coerce event_time if present
    if 'event_time' in df.columns:
        df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')
    return df


def sanitize_payments(df):
    if 'payment_date' in df.columns:
        df['payment_date'] = pd.to_datetime(df['payment_date'], errors='coerce')
    # clean trailing metadata in channel or other text fields
    for col in ['channel', 'payment_status']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"\s*\(.*\)$", '', regex=True).str.strip()
    # normalize amount to numeric
    if 'amount' in df.columns:
        df['amount'] = df['amount'].astype(str).str.replace(r"[^0-9.\-]", '', regex=True)
        df.loc[df['amount']=='', 'amount'] = '0'
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    return df


def main(args):
    outdir = args.outdir or 'out'
    os.makedirs(outdir, exist_ok=True)

    deliveries = load_table(args.delivery, DELIVERY_SAMPLE, parse_dates=['event_time'])
    payments = load_table(args.payments, PAYMENTS_SAMPLE, parse_dates=['payment_date'])

    deliveries = sanitize_delivery(deliveries)
    payments = sanitize_payments(payments)

    # basic stats
    print(f"Deliveries: {len(deliveries)} rows")
    if 'status' in deliveries.columns:
        print(deliveries['status'].value_counts(dropna=False).to_string())
    # determine currency if available
    currency = None
    if 'currency' in payments.columns:
        nonnull = payments['currency'].dropna().unique()
        if len(nonnull) > 0:
            currency = nonnull[0]
    total_pay_amount = payments['amount'].sum() if 'amount' in payments.columns else 0
    print(f"Payments: {len(payments)} rows; total amount: {total_pay_amount} {currency or ''}")

    # detect duplicate payments (same order_id, amount, payment_date)
    # choose keys for duplicate detection (fall back to order_id)
    dup_keys = []
    for k in ['order_id', 'package_id']:
        if k in payments.columns:
            dup_keys.append(k)
            break
    # always include amount and payment_date if present
    if 'amount' in payments.columns:
        dup_keys.append('amount')
    if 'payment_date' in payments.columns:
        dup_keys.append('payment_date')
    if dup_keys:
        payments['dup_group'] = payments[dup_keys].astype(str).agg('|'.join, axis=1)
    else:
        payments['dup_group'] = payments.index.astype(str)
    dup_counts = payments.groupby('dup_group').size().reset_index(name='count')
    duplicates = dup_counts[dup_counts['count'] > 1]
    if not duplicates.empty:
        print('\nDetected duplicate payment groups:')
        dup_groups = duplicates['dup_group'].tolist()
        dup_rows = payments[payments['dup_group'].isin(dup_groups)].drop(columns=['dup_group'])
        dup_rows.to_csv(os.path.join(outdir, 'duplicate_payments.csv'), index=False)
        print(dup_rows.head().to_string())
    else:
        print('\nNo duplicate payments detected')

    # join by order_id first
    # determine join keys: prefer explicit CLI args, else order_id then package_id
    join_keys = []
    if args.order_key:
        join_keys.append(args.order_key)
    elif 'order_id' in payments.columns and 'order_id' in deliveries.columns:
        join_keys.append('order_id')
    if args.package_key:
        join_keys.append(args.package_key)
    elif 'package_id' in payments.columns and 'package_id' in deliveries.columns:
        join_keys.append('package_id')

    if not join_keys:
        # no common join key — perform a Cartesian-like merge on nothing to align outputs
        merged = payments.merge(deliveries, how='outer', left_index=True, right_index=True, suffixes=('_pay', '_del'))
    else:
        merged = payments.merge(deliveries, on=join_keys, how='outer', suffixes=('_pay', '_del'))

    # payments without delivery (no event_id)
    payments_no_delivery = merged[merged.get('event_id').isna() if 'event_id' in merged.columns else merged['event_id'].isna()]
    payments_no_delivery.to_csv(os.path.join(outdir, 'payments_no_delivery.csv'), index=False)
    print(f"\nPayments without matching delivery: {len(payments_no_delivery)} (sample below)")
    print(payments_no_delivery.head().to_string())

    # deliveries without payments (no payment_id)
    deliveries_no_payment = merged[merged.get('payment_id').isna() if 'payment_id' in merged.columns else merged['payment_id'].isna()]
    deliveries_no_payment.to_csv(os.path.join(outdir, 'deliveries_no_payment.csv'), index=False)
    print(f"\nDeliveries without matching payment: {len(deliveries_no_payment)} (sample below)")
    print(deliveries_no_payment.head().to_string())

    # payments tied to returned/failed deliveries
    problem_status = ['RETURNED', 'FAILED']
    if 'status' in merged.columns:
        payments_with_problem_delivery = merged[merged['status'].isin(problem_status) & merged.get('payment_id').notna()]
    else:
        payments_with_problem_delivery = merged[merged.get('payment_id').notna()]
    payments_with_problem_delivery.to_csv(os.path.join(outdir, 'payments_with_problem_delivery.csv'), index=False)
    print(f"\nPayments with RETURNED/FAILED deliveries: {len(payments_with_problem_delivery)}")
    print(payments_with_problem_delivery.head().to_string())

    # save merged sample for inspection
    merged.to_csv(os.path.join(outdir, 'merged_sample.csv'), index=False)

    print(f"\nReports written to: {outdir}")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--delivery', help='Path to delivery CSV/TSV')
    p.add_argument('--payments', help='Path to payments CSV/TSV')
    p.add_argument('--outdir', help='Output directory', default='out')
    p.add_argument('--order-key', help='Column name to join on for order id (overrides auto-detect)')
    p.add_argument('--package-key', help='Column name to join on for package id (overrides auto-detect)')
    args = p.parse_args()
    main(args)
