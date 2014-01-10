
import csv
import datetime
import os
import logging

from .observer import Observer

KEY_ORDER = ['timestamp', 'market_1', 'market_2', 'market_1_ask', 'market_2_bid',
             'buy_price', 'sell_price', 'volume_btc', 'volume_usd', 'percent',
             'profit', 'weighted_buy', 'weighted_sell']


class MatrixCsvAccumulator(Observer):
    OUT_DIR = 'matrix/csv/'

    def __init__(self):
        self._depths = None
        self._start_time = datetime.datetime.utcnow()
        try:
            os.mkdir(self.OUT_DIR)
        except FileExistsError:
            pass
        filename = 'arb-opp-%d-%.2d-%.2dT%.2d%.2d%.2d.csv' % (
            self._start_time.year,
            self._start_time.month,
            self._start_time.day,
            self._start_time.hour,
            self._start_time.minute,
            self._start_time.second,
        )
        self._csv_file = open(self.OUT_DIR + filename, 'w')
        self._csv_writer = csv.DictWriter(self._csv_file, KEY_ORDER)
        self._csv_writer.writeheader()

    def begin_opportunity_finder(self, depths):
        self._depths = depths
        logging.info("Start opp")

    def end_opportunity_finder(self):
        logging.info("End opp")

    def opportunity(self, profit, volume, buy_price, kask, sell_price, kbid, perc, weighted_buy, weighted_sell):
        self._csv_writer.writerow(
          {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'market_1': kask,
            'market_2': kbid,
            'market_1_ask': self._depths[kask]['asks'][0]['price'],
            'market_2_bid': self._depths[kbid]['bids'][0]['price'],
            'buy_price': "%.2f" % buy_price,
            'sell_price': "%.2f" % sell_price,
            'volume_btc': "%.3f" % volume,
            'volume_usd': "%.2f" % (volume * buy_price),
            'percent': "%.2f" % perc,
            'profit': "%.2f" % profit,
            'weighted_buy': "%.2f" % weighted_buy,
            'weighted_sell': "%.2f" % weighted_sell
          }
        )
        self._csv_file.flush()

