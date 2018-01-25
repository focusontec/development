# coding=utf-8
a = ["http://www.worldcurling.org/congress2016", "http://www.worldcurling.org/2016-ecc-c-division",
     "http://www.worldcurling.org/wwcc2016", "http://www.worldcurling.org/wmxcc2016",
     "http://www.worldcurling.org/wmdcc2016", "http://www.worldcurling.org/wjcc2016",
     "http://www.worldcurling.org/wmcc2016", "http://www.worldcurling.org/wscc2016",
     "http://www.worldcurling.org/yog2016", "http://www.worldcurling.org/wwhcc2016",
     "http://www.worldcurling.org/world-junior-b-curling-championships-2016",
     "http://www.worldcurling.org/wwhcc2017/wwhbcc-live-scores", "http://www.worldcurling.org/ecc2016",
     "http://www.worldcurling.org/pacc2016"]
b = ["", "", "51", "109", "106", "103", "104", "105", "101", "102", "", "111", "112", "110"]
c = ["5th World Curling Congress", "European Curling Championships C-Division 2016",
     "Ford World Women's Curling Championship 2016", "World Mixed Curling Championship 2016",
     "World Mixed Doubles Curling Championship 2016", "VoIP Defender World Junior Curling Championships 2016",
     "World Men's Curling Championship 2016", "World Senior Curling Championships 2016", "Youth Olympic Games 2016",
     "World Wheelchair Curling Championship 2016", "World Junior-B Curling Championships 2016",
     "World Wheelchair-B Curling Championship 2016", "Le Gruyère AOP European Curling Championships 2016",
     "Pacific-Asia Curling Championships 2016"]
event_list = [{'event_href': x[0], 'event_id': x[1], 'event_name': x[2], 'event_abbr': ''} for x in zip(a, b, c)]
print event_list
event_list = [
    {'event_id': '', 'event_name': '5th World Curling Congress',
               'event_href': 'http://www.worldcurling.org/congress2016', 'event_abbr': ''},
              {'event_id': '', 'event_name': 'European Curling Championships C-Division 2016',
               'event_href': 'http://www.worldcurling.org/2016-ecc-c-division', 'event_abbr': ''},
              {'event_id': '51', 'event_name': "Ford World Women's Curling Championship 2016",
               'event_href': 'http://www.worldcurling.org/wwcc2016', 'event_abbr': 'WCF_WWCC2016PA'},
              {'event_id': '109', 'event_name': 'World Mixed Curling Championship 2016',
               'event_href': 'http://www.worldcurling.org/wmxcc2016', 'event_abbr': 'CUR_WMxCC2016P'},
              {'event_id': '106', 'event_name': 'World Mixed Doubles Curling Championship 2016',
               'event_href': 'http://www.worldcurling.org/wmdcc2016', 'event_abbr': 'CU_WMDCC2016P'},
              {'event_id': '103', 'event_name': 'VoIP Defender World Junior Curling Championships 2016',
               'event_href': 'http://www.worldcurling.org/wjcc2016', 'event_abbr': 'CU_WJCC2016P'},
              {'event_id': '104', 'event_name': "World Men's Curling Championship 2016",
               'event_href': 'http://www.worldcurling.org/wmcc2016', 'event_abbr': 'CU_WMCC2016P'},
              {'event_id': '105', 'event_name': 'World Senior Curling Championships 2016',
               'event_href': 'http://www.worldcurling.org/wscc2016', 'event_abbr': 'CU_WSCC2016P'},
              {'event_id': '101', 'event_name': 'Youth Olympic Games 2016',
               'event_href': 'http://www.worldcurling.org/yog2016', 'event_abbr': 'WYOG2016P'},
              {'event_id': '102', 'event_name': 'World Wheelchair Curling Championship 2016',
               'event_href': 'http://www.worldcurling.org/wwhcc2016', 'event_abbr': 'CU_WWhCC2016P'},
              {'event_id': '', 'event_name': 'World Junior-B Curling Championships 2016',
               'event_href': 'http://www.worldcurling.org/world-junior-b-curling-championships-2016', 'event_abbr': ''},
              {'event_id': '111', 'event_name': 'World Wheelchair-B Curling Championship 2016',
               'event_href': 'http://www.worldcurling.org/wwhcc2017/wwhbcc-live-scores', 'event_abbr': 'CUR_WWhCCB2016P'},
              {'event_id': '112', 'event_name': 'Le Gruy\xc3\xa8re AOP European Curling Championships 2016',
               'event_href': 'http://www.worldcurling.org/ecc2016', 'event_abbr': 'CUR_ECC2016P'},
              {'event_id': '110', 'event_name': 'Pacific-Asia Curling Championships 2016',
               'event_href': 'http://www.worldcurling.org/pacc2016', 'event_abbr': 'CUR_PACC2016P'}
]
