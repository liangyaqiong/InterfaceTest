
class Environment():
    def __init__(self):
        pass
    def enviro_get(self,env_key):
        if env_key =='PTC':  #env_key == 'PTC'
            base_url = 'http://qa-api-sqm-acct-ptc.qingchunbank.com:30007/com.omniprimeinc.ptc.ptc-server/ptc/'
        elif env_key == 'FUNDBASE':
            base_url = 'http://qa-api-fund-base.qingchunbank.com:30010/com.omniprimeinc.hawking.fundbase/'
        elif env_key =='FUNDLOAN':
            base_url = 'http://'
        elif env_key =='FUNDPOSTLOAN':
            base_url = 'qa-api-fund-core.qingchunbank.com:30005/fund-postloan/'
        elif env_key =='ADAPTER':
            base_url = 'http://qa-api-adapter.qingchunbank.com:30015/'
        elif env_key =='TRANSACTION':
            base_url = 'http://qa-api-transaction.qingchunbank.com:30002/finance-transaction/'
        elif env_key =='PHOEBUS':
            base_url = 'http://qa-api-sqm-acct-ptc.qingchunbank.com:30007/finance-settlement/settlement/'

        return base_url

en =Environment()
print(en.enviro_get('FUNDBASE'))