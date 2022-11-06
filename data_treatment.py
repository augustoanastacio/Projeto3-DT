import time

def data_treatment(json:list):
    # for index in json request output
    for i in range(len(json)):
        # runs through the keys of each list item 
        for key in json[i]:
            # if the key is a product
            if ('prod' in key):
                # if the value is not a dict, it means that the treatment wasn't made
                if (type(json[i][key])!=dict):
                    # stores the quantity in the variable
                    qnt = json[i][key]
                    # in case it is a string, does the coercion to float
                    if (type(qnt)==str):
                        qnt = float(qnt)   
                    # if the quantity is a negative value, it is corrected to zero
                    if (qnt<0):
                        qnt = 0
                        # substitutes the value for a dictionary containing the quantity and the price
                        json[i][key] = {'qnt':[qnt], 'price':None} 
                    else:
                        json[i][key] = {'qnt':[qnt], 'price':None} 
        try:
            # format date 
            json[i]['date'] = time.ctime(json[i]['date'])
        except:
            continue
    return json
