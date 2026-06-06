/**
 * API client for communicating with the backend
 */

const getApiBaseUrl = () => {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    if (hostname === 'eab.dev-hsh.online') {
      return 'https://eab-backend.dev-hsh.online';
    }
    if (hostname.startsWith('eab.')) {
      return `https://${hostname.replace('eab.', 'eab-backend.')}`;
    }
  }
  return process.env.NEXT_PUBLIC_API_URL || '';
};

const API_BASE_URL = getApiBaseUrl();

export interface EmotionAnalysis {
  text: string;
  emotion: string;
  confidence: number;
  emoji: string;
  color: string;
  count?: number;
  language?: string;  // 'en' for English, 'my' for Myanmar
  recommendations: {
    send_message: string;
    action: string;
    sources?: any;
    quick_action?: any;
  };
  source: 'ai' | 'rules';
  method?: string;
  scores?: {
    negative: number;
    neutral: number;
    positive: number;
    compound: number;
  };
  multi_source?: {
    emotion: string;
    sources: any;
    quick_action?: any;
    send_message?: string;
  };
  external_resources?: {
    emotion: string;
    sources: any;
    quick_picks?: any;
  };
}

export interface ApiError {
  detail: string;
}

/**
 * Analyze text for emotion detection
 */
export async function analyzeText(
  text: string,
  useAi: boolean = true,
  method: 'vader' | 'hmm' | 'hybrid' = 'vader'
): Promise<EmotionAnalysis> {
  const response = await fetch(`${API_BASE_URL}/api/detect/text`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text, use_ai: useAi, method }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail || 'Failed to analyze text');
  }

  return response.json();
}

/**
 * Analyze voice audio for emotion detection
 */
export async function analyzeVoice(
  audioBase64: string,
  useAi: boolean = true
): Promise<EmotionAnalysis> {
  const response = await fetch(`${API_BASE_URL}/api/detect/voice`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ audio_base64: audioBase64, use_ai: useAi }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail || 'Failed to analyze voice');
  }

  return response.json();
}

/**
 * Analyze captured face image for emotion detection
 */
export async function analyzeImage(
  imageBase64: string,
  language: string = "en"
): Promise<EmotionAnalysis> {
  const response = await fetch(`${API_BASE_URL}/api/detect/image`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: imageBase64, language }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail || 'Image analysis failed');
  }

  return response.json();
}

/**
 * Check API health status
 */
export async function checkHealth(): Promise<{
  status: string;
  ai_available: boolean;
  hmm_available: boolean;
  message: string;
}> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error('Health check failed');
  }

  return response.json();
}
/**
 * Analyze a social message for relationship advice
 */
export async function analyzeSocialMessage(
  message: string,
  perspective: 'receiver' | 'sender' = 'receiver',
  language: string = 'en'
): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/social/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, perspective, language }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail || 'Failed to analyze social message');
  }

  return response.json();
}
