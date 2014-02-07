from gdata.spreadsheet.service import SpreadsheetsService

import pdb

key = '0Ar4H2kiPmGtNdFBWa2FlalVONHpKaTlMekFvTThkeEE'

client = SpreadsheetsService()
feed = client.GetCellsFeed(key, visibility='public', projection='basic')

pdb.set_trac()
# need to figure out how to grab cells from here
