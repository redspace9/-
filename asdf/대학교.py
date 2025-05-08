import pandas as pd
import requests
import folium

# VWorld API 키 설정
VWORLD_API_KEY = 'YOUR_VWORLD_API_KEY'

# 주소를 위도/경도로 변환하는 함수
def get_coords_vworld(address):
    url = "https://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getcoord",
        "format": "json",
        "crs": "EPSG:4326",  # WGS84 (위도/경도)
        "key": VWORLD_API_KEY,
        "type": "ROAD",  # 도로명 주소, 지번 주소는 "PARCEL"
        "address": address
    }

    response = requests.get(url, params=params)
    result = response.json()

    try:
        if result['response']['status'] == 'OK':
            x = float(result['response']['result']['point']['x'])  # 경도
            y = float(result['response']['result']['point']['y'])  # 위도
            return y, x
    except Exception as e:
        print(f"주소 변환 실패: {address} → {e}")
    return None, None


df = pd.read_excel('고등교육기관_주소록.xlsx', header=5)
print(df.columns)  # 열 이름(헤더) 전체 출력

df['위도'], df['경도'] = zip(*df['주소'].apply(get_coords_vworld))


m = folium.Map(location=[37.5665, 126.9780], zoom_start=8)


for _, row in df.iterrows():
    if pd.notnull(row['위도']) and pd.notnull(row['경도']):
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=row['학교명'],
            tooltip=row['학교명']
        ).add_to(m)

# HTML로 저장
m.save("학교_지도_vworld.html")