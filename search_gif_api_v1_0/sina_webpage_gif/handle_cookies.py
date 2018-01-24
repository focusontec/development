cookies = "SUB=_2A253K_yiDeRhGeBK6VQR9SvKyjiIHXVUQWlqrDV8PUNbmtAKLRjdkW9NR8wwiheVNwdc78xjaJDcfHCPiO6C3vND; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWazoCIzaVUG3aec-jd-FWF5JpX5K2hUgL.FoqXeoq7SK-ceKB2dJLoI7yJdcSfMNxLq7tt; login_sid_t=26db486473310a5334d7a1fbc8ef2eb8; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=8324640846746.8125.1513065581718; SINAGLOBAL=8324640846746.8125.1513065581718; ULV=1513065581721:1:1:1:8324640846746.8125.1513065581718:; WBtopGlobal_register_version=49306022eb5a5f0b; UOR=,,graph.qq.com; SCF=AhXgMQh0b8yguq1ThdmlPjRJhJ2FmiHbUascamvwlfpP76sT8druxEtpqwzWBxWTbQYSzHHtH2ZBHWk8mUwuOQQ.; SUHB=0WGcbKrUfIKb_c; ALF=1513670514; SSOLoginState=1513065714; un=18864932834; SWB=usrmdinst_22; wvr=6; SWBSSL=usrmdinst_8; WBStorage=81fd372985034324|undefined"


def get_cookie(str):
    a = str.split('; ')
    temp_dict = {}
    for item in a:
        temp_dict[item.split('=')[0]] =  item.split('=')[1]
    return temp_dict


