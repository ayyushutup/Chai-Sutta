// Hyperlocal City Intelligence Platform API Client
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface WeatherData {
  temperature: number;
  humidity: number;
  wind_speed: number;
  rain: number;
  condition: string;
  severity: string;
  weather_code?: number | null;
  recorded_at: string;
}

export interface TrafficPoint {
  road_name?: string | null;
  current_speed: number;
  free_flow_speed: number;
  congestion_level: 'light' | 'moderate' | 'heavy' | 'gridlock' | string;
  source: string;
  recorded_at: string;
}

export interface CityMoodData {
  mood: string;
  mood_score: number;
  mood_emoji: string;
  factors: Record<string, any>;
}

export interface NewsItem {
  id: string;
  title: string;
  summary?: string | null;
  source_url: string;
  source_name: string;
  category: string;
  importance_score: number;
  published_at?: string | null;
  created_at: string;
}

export interface CommunityReport {
  id: string;
  content: string;
  category: string;
  severity: string;
  upvotes: number;
  downvotes: number;
  verification_status: string;
  media_type: string;
  media_url?: string | null;
  created_at: string;
}

export interface CityEvent {
  id: string;
  title: string;
  description?: string | null;
  category: string;
  starts_at: string;
  ends_at?: string | null;
  source: string;
}

export interface ChatReply {
  reply: string;
  sources?: any[];
  suggested_followups?: string[];
}

// Generic Fetch Wrapper with Automatic Offline Fallback
async function fetchWithFallback<T>(endpoint: string, fallbackData: T): Promise<T> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      signal: controller.signal,
      headers: {
        'Accept': 'application/json',
      },
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      console.warn(`API [${endpoint}] returned status ${response.status}. Using fallback telemetry.`);
      return fallbackData;
    }

    const data = await response.json();
    return data as T;
  } catch (err) {
    console.info(`API [${endpoint}] unavailable (${(err as Error).message}). Active telemetry running in offline fallback mode.`);
    return fallbackData;
  }
}

// API Service Endpoint Functions

export async function getCityWeather(city: string): Promise<WeatherData> {
  const fallback: WeatherData = {
    temperature: 31,
    humidity: 78,
    wind_speed: 18,
    rain: 0.2,
    condition: 'Thunderstorms likely near coastal areas',
    severity: 'moderate',
    recorded_at: new Date().toISOString(),
  };
  return fetchWithFallback<WeatherData>(`/weather/${encodeURIComponent(city)}`, fallback);
}

export async function getCityTraffic(city: string): Promise<TrafficPoint[]> {
  const fallback: TrafficPoint[] = [
    { road_name: 'Western Express Highway', current_speed: 18, free_flow_speed: 60, congestion_level: 'heavy', source: 'TomTom', recorded_at: new Date().toISOString() },
    { road_name: 'Eastern Freeway', current_speed: 52, free_flow_speed: 60, congestion_level: 'light', source: 'TomTom', recorded_at: new Date().toISOString() },
    { road_name: 'SV Road Bandra', current_speed: 12, free_flow_speed: 40, congestion_level: 'gridlock', source: 'TomTom', recorded_at: new Date().toISOString() },
    { road_name: 'BKC Connector', current_speed: 35, free_flow_speed: 50, congestion_level: 'moderate', source: 'TomTom', recorded_at: new Date().toISOString() },
  ];
  return fetchWithFallback<TrafficPoint[]>(`/traffic/${encodeURIComponent(city)}`, fallback);
}

export async function getCityMood(city: string): Promise<CityMoodData> {
  const fallback: CityMoodData = {
    mood: 'energetic',
    mood_score: 84,
    mood_emoji: '⚡',
    factors: { news_sentiment: 0.75, traffic_stress: -0.2, weather_comfort: 0.8 },
  };
  return fetchWithFallback<CityMoodData>(`/city-mood/${encodeURIComponent(city)}`, fallback);
}

export async function getNewsFeed(city: string, category?: string): Promise<NewsItem[]> {
  const query = category ? `?category=${encodeURIComponent(category)}` : '';
  const fallback: NewsItem[] = [
    { id: '1', title: 'Monsoon Alert: High Tide expected along Marine Drive & Worli Seaface at 4:30 PM', summary: 'BMC issues advisory for coastal areas with wave height predicted up to 4.2m.', source_name: 'Chai Sutta Radar', source_url: '#', category: 'Civic', importance_score: 95, created_at: '10 mins ago' },
    { id: '2', title: 'Western Railway increases AC Local train frequency during peak evening commute hours', summary: '12 new services added between Churchgate and Virar starting this Friday.', source_name: 'Rail Pulse', source_url: '#', category: 'Transit', importance_score: 88, created_at: '25 mins ago' },
    { id: '3', title: 'BKC Tech Hub expands electric shuttle service for corporate commuters', summary: 'Zero-emission last-mile connectivity now deployed across 14 office towers.', source_name: 'Urban Tech Today', source_url: '#', category: 'Tech', importance_score: 72, created_at: '1 hour ago' },
  ];
  
  const res = await fetchWithFallback<any>(`/news/feed/${encodeURIComponent(city)}${query}`, fallback);
  return Array.isArray(res) ? res : (res.items || fallback);
}

export async function getCommunityReports(city: string): Promise<CommunityReport[]> {
  const fallback: CommunityReport[] = [
    { id: 'rep-1', content: 'Waterlogging near Milan Subway underpass. Light vehicles advised to divert via SV Road.', category: 'Waterlogging', severity: 'heavy', upvotes: 42, downvotes: 2, verification_status: 'verified', media_type: 'none', created_at: '15 mins ago' },
    { id: 'rep-2', content: 'Signal malfunction at Dadar TT Circle causing slow-moving traffic on Tilak Bridge.', category: 'Traffic Signal', severity: 'moderate', upvotes: 28, downvotes: 1, verification_status: 'verified', media_type: 'none', created_at: '35 mins ago' },
    { id: 'rep-3', content: 'Fallen tree branch cleared near Hiranandani Powai Main Gate. Lane restored.', category: 'Obstruction', severity: 'light', upvotes: 19, downvotes: 0, verification_status: 'resolved', media_type: 'none', created_at: '1 hour ago' },
  ];
  
  const res = await fetchWithFallback<any>(`/reports/?city=${encodeURIComponent(city)}`, fallback);
  return Array.isArray(res) ? res : (res.items || fallback);
}

export async function getCityEvents(city: string): Promise<CityEvent[]> {
  const fallback: CityEvent[] = [
    { id: 'ev-1', title: 'Kala Ghoda Street Culture & Arts Festival 2026', description: 'Hyperlocal art installations and live indie music performances.', category: 'Cultural', starts_at: 'Tomorrow, 5:00 PM', source: 'City Digest' },
    { id: 'ev-2', title: 'Tech Startups & Founder Tapri Meetup', description: 'Casual networking over cutting chai at Prithvi Cafe Juhu.', category: 'Meetup', starts_at: 'Saturday, 11:00 AM', source: 'Chai Network' },
  ];
  return fetchWithFallback<CityEvent[]>(`/events/?city=${encodeURIComponent(city)}`, fallback);
}

export async function sendChatMessage(message: string, city: string): Promise<ChatReply> {
  const fallback: ChatReply = {
    reply: `Based on real-time city telemetry for ${city}: Weather is currently around 31°C with moderate humidity. Traffic on main arterial corridors like WEH is heavy, while Eastern Freeway is moving smoothly.`,
    sources: [{ title: 'City Live Sensors', category: 'Telemetry' }],
    suggested_followups: ['Show live traffic routes', 'What is the rain prediction?', 'Any local train delays?'],
  };

  try {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, city_name: city }),
    });
    if (!response.ok) return fallback;
    return (await response.json()) as ChatReply;
  } catch {
    return fallback;
  }
}
