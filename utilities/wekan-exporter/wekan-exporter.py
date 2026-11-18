#!/usr/bin/env python3
"""Prometheus exporter for Wekan.

Reads card counts per board/list directly from the Wekan MongoDB and exposes
them in Prometheus text format over HTTP:

    wekan_cards{board_title="work", list_title="Новые", status="active"} 3
    wekan_cards{board_title="work", list_title="Новые", status="archive"} 18
    wekan_exporter_up 1

Boards to export are taken from boards_data.yml (see --boards-file).
"""

import argparse
import os
import sys
import time

import yaml
from pymongo import MongoClient
from prometheus_client import REGISTRY, start_http_server
from prometheus_client.metrics_core import GaugeMetricFamily

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class WekanCollector:
    """Custom Prometheus collector that counts Wekan cards in MongoDB."""

    def __init__(self, mongo_uri, boards_file, db_name='wekan', cache_ttl=10.0):
        self.mongo_uri = mongo_uri
        self.boards_file = boards_file
        self.db_name = db_name
        self.cache_ttl = cache_ttl
        self._client = None
        self._boards = None
        self._boards_mtime = None
        self._cache = []  # cached samples of the last successful scrape
        self._cache_ts = 0.0

    # -- data collection -------------------------------------------------

    def _get_db(self):
        if self._client is None:
            self._client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self._client.admin.command('ping')
        return self._client[self.db_name]

    def _load_boards(self):
        """Load boards from YAML, reloading the file when it changes."""
        mtime = os.path.getmtime(self.boards_file)
        if self._boards is None or mtime != self._boards_mtime:
            with open(self.boards_file) as file:
                self._boards = yaml.safe_load(file) or []
            self._boards_mtime = mtime
        return self._boards

    def _fetch_metrics(self):
        db = self._get_db()
        boards = self._load_boards()

        lists_data = {}
        lists_collection = db['lists']
        for board in boards:
            query = {'boardId': board['_id']}
            projection = {'title': 1}
            lists_data[board['title']] = list(lists_collection.find(query, projection))

        # Count active/archive cards for all lists in one aggregation per board.
        cards_collection = db['cards']
        metrics_data = []
        for board_title, lists in lists_data.items():
            list_ids = [lst['_id'] for lst in lists]
            counts = {}
            if list_ids:
                pipeline = [
                    {'$match': {'listId': {'$in': list_ids}}},
                    {'$group': {
                        '_id': {'listId': '$listId', 'archived': '$archived'},
                        'count': {'$sum': 1},
                    }},
                ]
                for row in cards_collection.aggregate(pipeline):
                    key = (row['_id']['listId'], bool(row['_id'].get('archived')))
                    counts[key] = row['count']
            for lst in lists:
                metrics_data.append((board_title, lst['title'], 'active',
                                     counts.get((lst['_id'], False), 0)))
                metrics_data.append((board_title, lst['title'], 'archive',
                                     counts.get((lst['_id'], True), 0)))
        return metrics_data

    # -- Prometheus collector interface -----------------------------------

    def collect(self):
        gauge = GaugeMetricFamily(
            'wekan_cards',
            'Number of cards in a Wekan list',
            labels=['board_title', 'list_title', 'status'],
        )
        up = GaugeMetricFamily('wekan_exporter_up', 'Exporter could scrape Wekan MongoDB')

        now = time.monotonic()
        if self._cache and now - self._cache_ts < self.cache_ttl:
            samples = self._cache
        else:
            try:
                samples = self._fetch_metrics()
                self._cache = samples
                self._cache_ts = now
            except Exception as exc:  # noqa: BLE001 - report scrape failure to Prometheus
                print(f'error scraping Wekan MongoDB: {exc}', file=sys.stderr)
                samples = self._cache  # serve last known values
                up.add_metric([], 0)
                yield up
                for board_title, list_title, status, count in samples:
                    gauge.add_metric([board_title, list_title, status], count)
                yield gauge
                return

        up.add_metric([], 1)
        yield up
        for board_title, list_title, status, count in samples:
            gauge.add_metric([board_title, list_title, status], count)
        yield gauge


def parse_args():
    parser = argparse.ArgumentParser(description='Wekan Prometheus exporter')
    parser.add_argument(
        '--port', type=int,
        default=int(os.environ.get('WEKAN_EXPORTER_PORT', 9464)),
        help='HTTP port for /metrics (default: 9464)')
    parser.add_argument(
        '--mongo-uri',
        default=os.environ.get('WEKAN_MONGO_URI', 'mongodb://localhost:27017'),
        help='MongoDB connection URI (default: mongodb://localhost:27017)')
    parser.add_argument(
        '--db',
        default=os.environ.get('WEKAN_MONGO_DB', 'wekan'),
        help='Wekan database name (default: wekan)')
    parser.add_argument(
        '--boards-file',
        default=os.environ.get('WEKAN_BOARDS_FILE', os.path.join(BASE_PATH, 'boards_data.yml')),
        help='YAML file with boards to export (default: boards_data.yml next to the script)')
    parser.add_argument(
        '--cache-ttl', type=float,
        default=float(os.environ.get('WEKAN_EXPORTER_CACHE_TTL', 10)),
        help='seconds to reuse scrape results between /metrics requests (default: 10)')
    return parser.parse_args()


def main():
    args = parse_args()
    REGISTRY.register(WekanCollector(
        mongo_uri=args.mongo_uri,
        boards_file=args.boards_file,
        db_name=args.db,
        cache_ttl=args.cache_ttl,
    ))
    print(f'Serving Wekan metrics on http://0.0.0.0:{args.port}/metrics')
    start_http_server(args.port)
    while True:
        time.sleep(3600)


if __name__ == '__main__':
    main()
