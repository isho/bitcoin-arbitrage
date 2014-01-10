
import os
import re

from bs4 import BeautifulSoup

BASE_PATH = "matrix"
FILE_LIST = os.listdir(os.path.join(BASE_PATH, "html"))
KEY_ORDER = ['timestamp', 'market_1', 'market_2', 'Buy price',
             'Sell price', 'volume (BTC)', 'volume (USD)',
             'Percentage', 'profit', 'Weighted Buy', 'Weighted Sell']

def do_conversion():


  print(",".join(KEY_ORDER))

  for file in sorted(FILE_LIST):
    if re.match(r".*\.html$", file):
      with open(os.path.join(BASE_PATH, "html", file), errors='replace') as f:
        csv_values = {}
        soup = BeautifulSoup(f)
        table = soup.table
        csv_values['timestamp'] = soup.title.contents[0].split(" ")[-1]
        column_labels = [x.contents[0] if x.contents else None for x in table.tr('td')]
        for i, row in enumerate(table('tr')):
          row_cells =  row('td')
          if row.td.contents: # If the row has a label
            csv_values['market_1'] = row.td.contents[0]
            for i, td_cell in enumerate(row_cells):
              if i > 0 and td_cell.contents:
                csv_values['market_2'] = column_labels[i]
                for div_content in td_cell('div'):
                  parts = div_content.contents[0].split(':')
                  key = parts[0].strip()
                  value = parts[1].strip()
                  csv_values[key] = value
                print(",".join([csv_values[k] for k in KEY_ORDER]))

            # End content cells
          else:
            assert(i == 0)
        # End row

if __name__ == '__main__':
  do_conversion()