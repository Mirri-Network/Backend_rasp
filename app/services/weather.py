import requests, json, pandas as pd, os, asyncio
from dotenv import load_dotenv
from datetime import datetime

os.environ.clear()
load_dotenv()
api_key = os.getenv('API_KEY')
city_name = "Busan"
limit = 5

weather_data = {}

def fetch_weather_data():
    # 위치 데이터 가져오기
    get_location = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api_key}'
    location = requests.get(get_location).json()
    lat = location[0]['lat']
    lon = location[0]['lon']

    # 날씨 데이터 가져오기
    get_data = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}'
    data = requests.get(get_data).json()
    return data

def parse_weather_data(data):
    # 날씨 데이터 처리
    df = pd.DataFrame(data['list'])
    df['datetime'] = pd.to_datetime(df['dt'], unit='s')
    df['date'] = df['datetime'].dt.date
    df['temp'] = df['main'].apply(lambda x: x['temp'])
    df['weather'] = df['weather'].apply(lambda x: x[0]['main'])
    
    # 일별 요약 데이터 생성
    daily_summary = df.groupby('date').agg(
        max_temp=('temp', 'max'),
        min_temp=('temp', 'min'),
        weather_condition=('weather', lambda x: 'Rain' if 'Rain' in x.values else ('Clear' if 'Clear' in x.values else 'Clouds'))
    ).reset_index()

    # JSON 형식으로 변환, date를 문자열로 변환
    daily_summary['date'] = daily_summary['date'].astype(str)
    daily_summary_json = daily_summary.to_dict(orient='records')

    # 오늘의 최신 날씨 데이터, datetime을 문자열로 변환
    today_data = df[df['date'] == datetime.now().date()]
    if not today_data.empty:
        current_weather = today_data.iloc[-1][['datetime', 'temp', 'weather']].to_dict()
        current_weather['datetime'] = current_weather['datetime'].strftime('%Y-%m-%d %H:%M:%S')
    else:
        current_weather = None
    
    # 결과 반환
    return {
        "daily_summary": daily_summary_json,
        "current_weather": current_weather
    }

# SSE를 통해 날씨 데이터를 전송하는 함수
async def weather_sse():
    global weather_data
    last_updated_hour = None  # 마지막으로 데이터를 업데이트한 시간

    while True:
        now = datetime.now()
        
        # 매 정시에 데이터 갱신
        if not weather_data or now.hour != last_updated_hour:
            raw_data = fetch_weather_data()
            weather_data = parse_weather_data(raw_data)
            last_updated_hour = now.hour
            print(f"Updated data: {json.dumps(weather_data, indent=4)}")

        # 저장된 데이터를 클라이언트로 전송
        yield f"data: {json.dumps(weather_data)}\n\n"

        # 10초 대기
        await asyncio.sleep(10)
