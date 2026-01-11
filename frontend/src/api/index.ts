export interface GetAllClassesRequest {
  title?: string | null;
  instructor?: string | null;
  studios?: string[] | null;
  style?: string | null;
  date?: string | null;
  start_time?: string | null;
  end_time?: string | null;
  difficulty?: string | null;
  cancelled?: boolean | null;
  page: number;
  limit: number;
}

export interface DanceClass {
  title: string;
  instructor: string;
  studio: string;
  style: string;
  date: string;
  start_time: string;
  end_time: string;
  difficulty: string;
  cancelled: boolean;
}

export type GetAllClassesResponse = DanceClass[];

export async function get_all_classes(
  request: GetAllClassesRequest
): Promise<GetAllClassesResponse> {
  const params = new URLSearchParams();

  Object.entries(request).forEach(([key, value]) => {
    if (value === null || value === undefined) return;

    if (Array.isArray(value)) {
      value.forEach(v => params.append(key, String(v)));
    } else {
      params.append(key, String(value));
    }
  });

  try {
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
    const response = await fetch(`${backendUrl}/?${params.toString()}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('Failed to fetch classes:', error);
    throw error;
  }
}
