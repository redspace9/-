import pandas as pd
import requests
import folium

VWORLD_API_KEY = 'YOUR_VWORLD_API_KEY'

def get_coords_vworld(address):
    url = "https://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getcoord",
        "format": "json",
        "crs": "EPSG:4326",
        "key": VWORLD_API_KEY,
        "type": "ROAD", 
        "address": address
    }

    response = requests.get(url, params=params)
    result = response.json()

    try:
        if result['response']['status'] == 'OK':
            x = float(result['response']['result']['point']['x'])  
            y = float(result['response']['result']['point']['y'])  
            return y, x
    except Exception as e:
        print(f"주소 변환 실패: {address} → {e}")
    return None, None

df = pd.read_excel('고등교육기관_주소록.xlsx', header=5)
print(df.columns)

df['위도'], df['경도'] = zip(*df['주소'].apply(get_coords_vworld))

m = folium.Map(location=[37.5665, 126.9780], zoom_start=8)

for _, row in df.iterrows():
    if pd.notnull(row['위도']) and pd.notnull(row['경도']):
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=row['학교명'],
            tooltip=row['학교명']
        ).add_to(m)

campus_address = "광주광역시 북구 하서로 429"
lat, lon = get_coords_vworld(campus_address)

if lat and lon:
    folium.Marker(
        location=[lat, lon],
        popup="광주폴리텍대학 광주캠퍼스",
        tooltip="광주폴리텍대학 광주캠퍼스"
    ).add_to(m)
else:
    print("광주폴리텍대학 광주캠퍼스 주소 변환 실패")

# HTML 저장
m.save("학교_지도_vworld.html")
