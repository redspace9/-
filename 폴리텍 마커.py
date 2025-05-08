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

# '한국폴리텍 대학 광주캠퍼스' 주소
address = "광주광역시 북구 용봉로 110 한국폴리텍대학교 광주캠퍼스"

# 좌표 얻기
lat, lng = get_coords_vworld(address)
print(f"위도: {lat}, 경도: {lng}")

# 지도 생성 (서울 중심으로 시작)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=8)

# 마커 추가
if lat and lng:
    folium.Marker([lat, lng], tooltip="한국폴리텍 대학 광주캠퍼스").add_to(m)

# HTML 파일로 저장
m.save("gwangju_polytechnic_campus_map.html")

# 지도 확인 (Jupyter Notebook 환경에서는 맵을 직접 띄울 수 있습니다)
m
