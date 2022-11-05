import time

def data_treatment(json:list):
    for i in range(len(json)):
        for key in json[i]:
            if ('prod' in key):
                if (type(json[i][key])!=dict):
                    qnt = json[i][key]
                    if (type(qnt)==str):
                        qnt = float(qnt)                  
                    if (qnt<0):
                        qnt = 0
                        json[i][key] = {'qnt':qnt, 'price':None}
                    else:
                        json[i][key] = {'qnt':qnt, 'price':None}
        try:
            json[i]['date'] = time.ctime(json[i]['date'])
        except:
            continue
    return json