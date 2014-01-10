import logging
from .observer import Observer


class Logger(Observer):
    def opportunity(self, profit, volume, buyprice, kask, sellprice, kbid, perc,
                    weighted_buyprice, weighted_sellprice):
        logging.info(
            "profit: %.2f USD with volume: %.4f BTC (%.2f USD) - "
            "buy at %.4f (%s) sell at %.4f (%s) ~%.2f%%" % (
                profit, volume, volume*buyprice, buyprice, kask, sellprice, kbid, perc))
