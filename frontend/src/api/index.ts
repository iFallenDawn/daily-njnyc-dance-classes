export interface GetAllClassesRequest {
  title?: string | null;
  instructors?: string[] | null;
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
    const backendUrl =
      import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
    const response = await fetch(`${backendUrl}/?${params.toString()}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error("Failed to fetch classes:", error);
    throw error;
  }
}

// Fetch all unique instructors (for filter dropdown)
export async function get_all_instructors(): Promise<string[]> {
  try {
    const backendUrl =
      import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

    // Fetch first page to get metadata (total_pages, total_count)
    const firstResponse = await fetch(`${backendUrl}/?page=1&limit=50`);

    if (!firstResponse.ok) {
      throw new Error(`HTTP error! status: ${firstResponse.status}`);
    }

    const firstResult: GetAllClassesResponse = await firstResponse.json();
    const allInstructors = new Set<string>();

    // Add instructors from first page
    firstResult.data.forEach((danceClass) => {
      if (danceClass.instructor) {
        allInstructors.add(danceClass.instructor);
      }
    });

    // Use metadata to determine how many more pages to fetch
    const { total_pages } = firstResult;

    if (total_pages > 1) {
      // Fetch remaining pages in parallel
      const pagePromises = [];
      for (let page = 2; page <= total_pages; page++) {
        pagePromises.push(
          fetch(`${backendUrl}/?page=${page}&limit=50`).then((res) =>
            res.json()
          )
        );
      }

      const remainingResults: GetAllClassesResponse[] = await Promise.all(
        pagePromises
      );

      // Add instructors from all remaining pages
      remainingResults.forEach((result) => {
        result.data.forEach((danceClass) => {
          if (danceClass.instructor) {
            allInstructors.add(danceClass.instructor);
          }
        });
      });
    }

    return Array.from(allInstructors).sort();
  } catch (error) {
    console.error("Failed to fetch instructors:", error);
    return [];
  }
}
