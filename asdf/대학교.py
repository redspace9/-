import pandas as pd
import requests
import folium

VWORLD_API_KEY = '045F12DC-C599-3BBE-8B81-181AA429AACB'

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
    
    # 응답 결과 출력
    print(f"주소: {address}")
    print(f"응답 결과: {result}")
    
    try:
        if result['response']['status'] == 'OK':
            x = float(result['response']['result']['point']['x'])  # 경도
            y = float(result['response']['result']['point']['y'])  # 위도
            return y, x
    except Exception as e:
        print(f"주소 변환 실패: {address} → {e}")
    
    return None, None

# 데이터프레임 읽기
df = pd.read_excel('고등교육기관_주소록.xlsx', header=5)
print(df.columns)

# 좌표 추가
df['위도'], df['경도'] = zip(*df['주소'].apply(get_coords_vworld))

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=8)

# 지도에 마커 추가
for idx, row in df.iterrows():
    if pd.notnull(row['위도']) and pd.notnull(row['경도']):
        folium.Marker([row['위도'], row['경도']], tooltip=row['학교명']).add_to(m)

# HTML 파일로 저장
m.save("map.html")

# 지도 확인 (Jupyter Notebook 환경에서는 맵을 직접 띄울 수 있습니다)
m
