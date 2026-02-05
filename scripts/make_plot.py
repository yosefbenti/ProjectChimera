#!/usr/bin/env python3
from io import StringIO
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DELIVERY_SAMPLE = (
    "event_id\tpackage_id\torder_id\tevent_time\tstatus\tcity\n"
    "D2001\tPK9001\tO5001\t2026-01-02 14:20\tDELIVERED\tAddis\n"
    "D2002\tPK9002\tO5002\t2026-01-03 16:10\tDELIVERED\tAddis\n"
    "D2003\tPK9003\tO5003\t2026-01-06 09:00\tDELIVERED\tAdama\n"
    "D2004\tPK9004\tO5004\t2026-01-06 18:30\tDELIVERED\tAddis\n"
    "D2005\tPK9005\tO5005\t2026-01-07 15:10\tDELIVERED\tBahirDar\n"
    "D2006\tPK9006\tO5006\t2026-02-01 10:05\tDELIVERED\tAddis\n"
    "D2007\tPK9007\tO5007\t2026-01-12 17:00\tDELIVERED\tAddis\n"
    "D2008\tPK9008\tO5008\t2026-01-15 13:45\tDELIVERED\tAddis\n"
    "D2009\tPK9009\tO5009\t2026-01-19 11:22\tDELIVERED\tAdama\n"
    "D2010\tPK9010\tO5010\t2026-01-20 16:00\tDELIVERED\tAddis\n"
    "D2011\tPK9011\tO5011\t2026-01-22 18:00\tDELIVERED\tAddis\n"
    "D2012\tPK9012\tO5012\t2026-01-23 15:40\tDELIVERED\tHawassa\n"
    "D2013\tPK9013\tO5013\t2026-01-24 12:00\tDELIVERED\tAddis\n"
    "D2014\tPK9014\tO5014\t2026-01-26 09:10\tDELIVERED\tAddis\n"
    "D2015\tPK9015\tO5015\t2026-01-26 17:50\tDELIVERED\tAddis\n"
    "D2016\tPK9016\tO5016\t2026-01-29 14:10\tFAILED\tAddis\n"
    "D2017\tPK9017\tO5017\t2026-01-29 19:00\tFAILED\tAddis\n"
    "D2018\tPK9018\tO5018\t2026-02-02 11:00\tDELIVERED\tAddis\n"
    "D2019\tPK9019\tO5019\t2026-02-03 16:40\tDELIVERED\tAddis\n"
    "D2020\tPK9020\tO5020\t2026-01-31 15:00\tRETURNED\tAddis\n"
    "D2021\tPK9024\tO5024\t2026-01-13 12:00\tDELIVERED\tAddis (See <attachments>)\n"
)

def make_plot(path='out/status_counts.png'):
    s = StringIO(DELIVERY_SAMPLE)
    df = pd.read_csv(s, sep='\t', engine='python')
    if 'city' in df.columns:
        df['city'] = df['city'].astype(str).str.replace(r"\s*\(.*\)$", '', regex=True).str.strip()
    counts = df['status'].value_counts()
    fig, ax = plt.subplots(figsize=(6,3))
    colors = ['#2ca02c' if x=='DELIVERED' else '#ff7f0e' if x=='FAILED' else '#d62728' for x in counts.index]
    counts.plot(kind='bar', color=colors, ax=ax)
    ax.set_title('Delivery Event Counts by Status')
    ax.set_ylabel('Count')
    ax.set_xlabel('Status')
    for i, v in enumerate(counts.values):
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom')
    fig.tight_layout()
    fig.savefig(path, dpi=150)

if __name__ == '__main__':
    import os
    os.makedirs('out', exist_ok=True)
    make_plot()
    print('Saved out/status_counts.png')
