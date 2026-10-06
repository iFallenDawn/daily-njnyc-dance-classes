"use client";

// react
import { useEffect, useState } from "react";

// data table stuff
import { columns } from "../components/class-table/columns";
import { DataTable } from "../components/class-table/data-table";

// api
import {
  get_all_classes,
  get_filter_options,
  type DanceClass,
} from "@/api/index";

// utils
import { formatDate, formatTime } from "@/lib/formatting";
import { format } from "date-fns";

// custom components
import { Pagination } from "@/components/class-table/pagination";
import SearchBar, {
  type FilterState,
} from "@/components/class-table/search-bar";

export default function Home() {
  const [data, setData] = useState<DanceClass[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Filter state
  const [filters, setFilters] = useState<FilterState>({
    title: "",
    studios: new Set<string>(),
    instructors: new Set<string>(),
    startDate: undefined,
    endDate: undefined,
    startTime: undefined,
    endTime: undefined,
  });

  // Available studios and instructors lists - fetched once on mount
  const [availableStudios, setAvailableStudios] = useState<string[]>([]);
  const [availableInstructors, setAvailableInstructors] = useState<string[]>(
    []
  );
  const [filterOptionsLoaded, setFilterOptionsLoaded] = useState(false);

  // Fetch all studios and instructors on mount
  useEffect(() => {
    const fetchFilterOptions = async () => {
      const { instructors, studios } = await get_filter_options();
      setAvailableInstructors(instructors);
      setAvailableStudios(studios);
      // Auto-select all studios and instructors on first load
      setFilters((prev) => ({
        ...prev,
        instructors:
          instructors.length > 0 ? new Set(instructors) : prev.instructors,
        studios: studios.length > 0 ? new Set(studios) : prev.studios,
      }));
      setFilterOptionsLoaded(true);
    };
    fetchFilterOptions();
  }, []);

  useEffect(() => {
    let isMounted = true;

    const fetchClasses = async () => {
      // Studios and instructors start empty until their options load, keep showing loading until then
      if (!filterOptionsLoaded) {
        return;
      }

      try {
        setLoading(true);
        setError(null);

        // If studios or instructors are completely empty, don't fetch - return empty results
        if (filters.studios.size === 0 || filters.instructors.size === 0) {
          if (isMounted) {
            setData([]);
            setTotalPages(1);
            setLoading(false);
          }
          return;
        }

        // Build request with filter parameters
        const response = await get_all_classes({
          page: currentPage,
          limit: 10,
          title: filters.title || null,
          instructors:
            filters.instructors.size > 0
              ? Array.from(filters.instructors)
              : null,
          studios:
            filters.studios.size > 0 ? Array.from(filters.studios) : null,
          style: null,
          date: null,
          start_time: filters.startDate
            ? format(filters.startDate, "yyyy-MM-dd'T'00:00:00")
            : null,
          end_time: filters.endDate
            ? format(filters.endDate, "yyyy-MM-dd'T'23:59:59")
            : null,
          start_time_of_day: filters.startTime ?? null,
          end_time_of_day: filters.endTime ?? null,
          difficulty: null,
          cancelled: null,
        });

        // format class dates and times
        response.data.forEach((danceClass) => {
          danceClass.date = formatDate(danceClass.start_time);
          danceClass.start_time = formatTime(danceClass.start_time);
          danceClass.end_time = formatTime(danceClass.end_time);
        });

        if (isMounted) {
          setData(response.data);
          setTotalPages(response.total_pages);
        }
      } catch (err) {
        if (isMounted) {
          setError(
            err instanceof Error ? err.message : "Failed to fetch classes"
          );
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchClasses();

    return () => {
      isMounted = false;
    };
  }, [currentPage, filters, filterOptionsLoaded]);

  // Reset to page 1 when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [filters]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  return (
    <div className="flex flex-col min-h-screen w-full max-w-6xl mx-auto px-4 py-6 md:h-screen md:py-8">
      {/* <ModeToggle /> */}
      <div className="flex flex-col mb-4">
        <div className="text-2xl font-semibold">Daily NJ/NYC Dance Class Schedule</div>
        <div className="text-muted-foreground">
          Browse and filter dance classes
        </div>
      </div>
      <SearchBar
        studios={availableStudios}
        instructors={availableInstructors}
        filters={filters}
        onFiltersChange={setFilters}
      />
      {error && <div className="text-red-500 mb-4">Error: {error}</div>}
      <div className="md:flex-1 md:overflow-auto md:min-h-0">
        <DataTable columns={columns} data={data} loading={loading} />
      </div>
      {totalPages > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
          disabled={loading}
        />
      )}
      <footer className="mt-4 text-center text-sm text-muted-foreground">
        Made by Jordan Wang and Ron Dumalagan ·{" "}
        <a
          href="https://github.com/iFallenDawn/daily-njnyc-dance-classes"
          target="_blank"
          rel="noopener noreferrer"
          className="underline underline-offset-4 hover:text-foreground"
        >
          GitHub
        </a>
      </footer>
    </div>
  );
}
