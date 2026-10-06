const API_URL = `${import.meta.env.VITE_BACKEND_URL ??
  (import.meta.env.DEV ? "http://localhost:8000" : "")
  }/api`;

export interface GetAllClassesRequest {
  title?: string | null;
  instructors?: string[] | null;
  studios?: string[] | null;
  style?: string | null;
  date?: string | null;
  start_time?: string | null;
  end_time?: string | null;
  start_time_of_day?: string | null;
  end_time_of_day?: string | null;
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

export interface GetAllClassesResponse {
  data: DanceClass[];
  page: number;
  total_pages: number;
  total_count: number;
  limit: number;
}

export async function get_all_classes(
  request: GetAllClassesRequest
): Promise<GetAllClassesResponse> {
  const params = new URLSearchParams();

  Object.entries(request).forEach(([key, value]) => {
    if (value === null || value === undefined) return;

    if (Array.isArray(value)) {
      value.forEach((v) => params.append(key, String(v)));
    } else {
      params.append(key, String(value));
    }
  });

  try {
    const response = await fetch(`${API_URL}/classes?${params.toString()}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error("Failed to fetch classes:", error);
    throw error;
  }
}

export interface FilterOptions {
  instructors: string[];
  studios: string[];
}

// Fetch all unique instructors and studios (for filter dropdowns)
export async function get_filter_options(): Promise<FilterOptions> {
  try {
    // Fetch first page to get metadata (total_pages, total_count)
    const firstResponse = await fetch(`${API_URL}/classes?page=1&limit=50`);

    if (!firstResponse.ok) {
      throw new Error(`HTTP error! status: ${firstResponse.status}`);
    }

    const firstResult: GetAllClassesResponse = await firstResponse.json();
    const allInstructors = new Set<string>();
    const allStudios = new Set<string>();

    const addFilterOptions = (danceClasses: DanceClass[]) => {
      danceClasses.forEach((danceClass) => {
        if (danceClass.instructor) {
          allInstructors.add(danceClass.instructor);
        }
        if (danceClass.studio) {
          allStudios.add(danceClass.studio);
        }
      });
    };

    // Add instructors and studios from first page
    addFilterOptions(firstResult.data);

    // Use metadata to determine how many more pages to fetch
    const { total_pages } = firstResult;

    if (total_pages > 1) {
      // Fetch remaining pages in parallel
      const pagePromises = [];
      for (let page = 2; page <= total_pages; page++) {
        pagePromises.push(
          fetch(`${API_URL}/classes?page=${page}&limit=50`).then((res) =>
            res.json()
          )
        );
      }

      const remainingResults: GetAllClassesResponse[] = await Promise.all(
        pagePromises
      );

      // Add instructors and studios from all remaining pages
      remainingResults.forEach((result) => addFilterOptions(result.data));
    }

    return {
      instructors: Array.from(allInstructors).sort(),
      studios: Array.from(allStudios).sort(),
    };
  } catch (error) {
    console.error("Failed to fetch filter options:", error);
    return { instructors: [], studios: [] };
  }
}
