# Reconciliation script

Run the delivery vs payments reconciliation script. If you don't pass file paths, the embedded sample data will be used.

Install:

```bash
python3 -m pip install -r requirements.txt
```

Run with samples:

```bash
python3 scripts/reconcile.py --outdir out
```

Run with your own files (CSV or TSV):

```bash
python3 scripts/reconcile.py --delivery path/to/delivery.tsv --payments path/to/payments.tsv --outdir out
```

Outputs will be written to the `out` directory: duplicate_payments.csv, payments_no_delivery.csv, deliveries_no_payment.csv, payments_with_problem_delivery.csv, merged_sample.csv
