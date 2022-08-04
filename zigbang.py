import requests
import pandas as pd
import geohash2

def oneroom(addr):
    # 1.해당 지역의 좌표 값을 얻는다.
    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q={addr}&serviceType=원룸"
    response = requests.get(url)
    data = response.json()['items'][0]
    lat, lng = data['lat'], data['lng']
    
    # 2. 좌표를 geohash로 뱐환 한다.
    geohash = geohash2.encode(lat, lng, precision=5)
    
    # 3. geohash 값으로 매물 ID를 얻는다.
    url = f"https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang\
&geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸"
    response = requests.get(url)
    items = response.json()['items']
    ids = [items['item_id'] for items in items]
    
    # 4. 매물 ID로 매물 정보를 얻는다
    url = "https://apis.zigbang.com/v2/items/list"
    params = {
        "domain" : "zigbang",
        "withCoalition" : "true",
        "item_ids" : ids[:900] 
    }

    response = requests.post(url,params)
    items = response.json()['items']
    
    #5.필요한 컬럼만 추가하여 DataFrame을 만든다.
    columns = ['item_id', 'sales_type','deposit','rent','size_m2','address1','manage_cost']
    
    return pd.DataFrame(items)[columns]
