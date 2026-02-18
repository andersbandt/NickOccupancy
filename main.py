#!/usr/bin/env python3
"""
Visualize Nicholas Rec Center occupancy data.

Usage:
    python main.py                      # plot the most recent day with data
    python main.py --date 2021-03-26    # plot a specific day
    python main.py --heatmap            # avg occupancy by weekday + hour
    python main.py --all                # plot all recorded data
"""

import sqlite3
import argparse
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

DB_PATH = 'data.db'


def load_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT DATETIME, OCCUPANCY FROM OCCUPANCY ORDER BY DATETIME')
    rows = cur.fetchall()
    conn.close()

    data = []
    for dt_str, occ in rows:
        dt = datetime.datetime.fromisoformat(dt_str)
        data.append((dt, int(occ)))
    return data


def plot_day(data, date):
    day_data = [(dt, occ) for dt, occ in data if dt.date() == date]
    if not day_data:
        print(f"No data for {date}")
        return

    times, occs = zip(*day_data)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(times, occs, color='steelblue', linewidth=2)
    ax.fill_between(times, occs, alpha=0.15, color='steelblue')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I %p'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gcf().autofmt_xdate()
    ax.set_ylim(0, 100)
    ax.set_ylabel('Occupancy (%)')
    ax.set_title(f'Nick Rec — {date.strftime("%A, %B %d %Y")}')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_heatmap(data):
    """Average occupancy by weekday (rows) and hour of day (columns)."""
    totals = np.zeros((7, 24))
    counts = np.zeros((7, 24))
    for dt, occ in data:
        totals[dt.weekday()][dt.hour] += occ
        counts[dt.weekday()][dt.hour] += 1

    with np.errstate(invalid='ignore'):
        avg = np.where(counts > 0, totals / counts, np.nan)

    fig, ax = plt.subplots(figsize=(14, 4))
    im = ax.imshow(avg, aspect='auto', cmap='YlOrRd', vmin=0, vmax=100)
    plt.colorbar(im, ax=ax, label='Avg Occupancy (%)')

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax.set_yticks(range(7))
    ax.set_yticklabels(days)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f'{h}:00' for h in range(0, 24, 2)], rotation=45)
    ax.set_xlabel('Hour of Day')
    ax.set_title('Nick Rec — Average Occupancy by Day & Hour')
    plt.tight_layout()
    plt.show()


def plot_all(data):
    times, occs = zip(*data)

    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(times, occs, linewidth=0.6, color='steelblue', alpha=0.7)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()
    ax.set_ylim(0, 100)
    ax.set_ylabel('Occupancy (%)')
    ax.set_title('Nick Rec — All Recorded Data')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Nick Rec Center occupancy graphs.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--date', type=datetime.date.fromisoformat, metavar='YYYY-MM-DD',
        help='Plot a specific date'
    )
    group.add_argument(
        '--heatmap', action='store_true',
        help='Heatmap of average occupancy by weekday and hour'
    )
    group.add_argument(
        '--all', action='store_true', dest='all_data',
        help='Plot all recorded data'
    )
    args = parser.parse_args()

    data = load_data()
    if not data:
        print("No data in database. Run nick.py first.")
        return

    if args.heatmap:
        plot_heatmap(data)
    elif args.all_data:
        plot_all(data)
    else:
        date = args.date or max(dt.date() for dt, _ in data)
        plot_day(data, date)


if __name__ == '__main__':
    main()
