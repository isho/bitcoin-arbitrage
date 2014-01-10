
import os
import time
import logging
from .observer import Observer


class MatrixHtmlAccumulator(Observer):
    OUT_DIR = 'matrix/html/'

    def __init__(self):
        self._matrix = None 
        self._markets = None
        self._start_time = None
        try:
            os.mkdir(self.OUT_DIR)
        except FileExistsError:
            pass
        
    def begin_opportunity_finder(self, depths):
        self._start_time = int(time.time())
        self._matrix = {}
        self._markets = list(depths.keys())
        self._markets.sort()

    def end_opportunity_finder(self):
        logging.info(self._matrix)
        filename = self.OUT_DIR + 'arb-opp-matrix-%s.html' % self._start_time
        fp = open(filename, 'w')
        fp.write("<html>")
        fp.write("<head><title>Arbitrage Opportunity Matrix %s</title></head>" % self._start_time)
        fp.write("<body>")
        fp.write('<table border="1">')
        fp.write("<tr><td></td>")
        # Write out the top row. Column labels
        for market in self._markets:
            fp.write("<td>%s</td>" % market)
        fp.write("</tr>")
        for market_row in self._markets:
            fp.write("<tr><td>%s</td>" % market_row) # Row label
            for market_col in self._markets:
                if market_row == market_col:
                    fp.write("<td></td>")
                else:
                    key = (market_row, market_col)
                    if key not in self._matrix:
                        fp.write("<td></td>")
                    else:
                        opp_data = self._matrix[key]
                        fp.write("<td>")
                        fp.write("<div>profit: %.2f</div>" % opp_data['profit'])
                        fp.write("<div>volume (BTC): %.3f</div>" % opp_data['volume'])
                        fp.write("<div>volume (USD): %.2f</div>" % (opp_data['volume'] * opp_data['buy_price']))
                        fp.write("<div>Buy price: %.3f</div>" % opp_data['buy_price'])
                        fp.write("<div>Sell price: %.3f</div>" % opp_data['sell_price'])
                        fp.write("<div>Percentage: %.2f%%</div>" % opp_data['percentage'])
                        fp.write("<div>Weighted Buy: %.2f</div>" % opp_data['weighted_buy'])
                        fp.write("<div>Weighted Sell: %.2f</div>" % opp_data['weighted_sell'])
                        fp.write("</td>")
                        
            fp.write("</tr>")
        fp.write("</table>")
        fp.write("</body></html>")
        fp.close()
        logging.info("*"*80)
        logging.info("*** Matrix output")
        logging.info("*"*80)

    def opportunity(self, profit, volume, buy_price, kask, sell_price, kbid, perc,
                    weighted_buy, weighted_sell):

        self._matrix[(kask, kbid)] = {
            "profit": profit,
            "volume": volume,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "percentage": perc,
            "weighted_buy": weighted_buy,
            "weighted_sell": weighted_sell,
        }


