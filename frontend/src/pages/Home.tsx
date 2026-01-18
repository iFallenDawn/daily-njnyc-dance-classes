"use client";

// react
import { useEffect, useState, useMemo } from "react";

// data table stuff
import { columns } from "../components/class-table/columns";
import { DataTable } from "../components/class-table/data-table";

// api
import {
  get_all_classes,
  get_all_instructors,
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
    studios: new Set<string>([
      "Modega",
      "ILoveDance Manhattan",
      "ILoveDance Queens",
      "ILoveDance New Jersey",
    ]),
    instructors: new Set<string>(),
    startDate: undefined,
    endDate: undefined,
    startTime: undefined,
    endTime: undefined,
  });

  // Known studios list - hardcoded since these are the only studios we scrape
  const availableStudios = useMemo(
    () => [
      "Modega",
      "ILoveDance Manhattan",
      "ILoveDance Queens",
      "ILoveDance New Jersey",
    ],
    []
  );

  // Available instructors list - fetched once on mount
  const [availableInstructors, setAvailableInstructors] = useState<string[]>(
    []
  );

  // Fetch all instructors on mount
  useEffect(() => {
    const fetchInstructors = async () => {
      const instructors = await get_all_instructors();
      setAvailableInstructors(instructors);
      // Auto-select all instructors on first load
      if (instructors.length > 0) {
        setFilters((prev) => ({
          ...prev,
          instructors: new Set(instructors),
        }));
      }
    };
    fetchInstructors();
  }, []);

  useEffect(() => {
    let isMounted = true;

    const fetchClasses = async () => {
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
  }, [currentPage, filters]);

  // Reset to page 1 when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [filters]);

  // Apply client-side filtering for time range only
  const filteredData = useMemo(() => {
    return data.filter((danceClass) => {
      // Time range filter - check if class time overlaps with selected range
      if (filters.startTime || filters.endTime) {
        try {
          const classStart24 = convertTo24Hour(danceClass.start_time);
          const classEnd24 = convertTo24Hour(danceClass.end_time);

          // Check if class overlaps with the filter range
          if (filters.startTime && classEnd24 < filters.startTime) {
            return false;
          }

          if (filters.endTime && classStart24 > filters.endTime) {
            return false;
          }
        } catch {
          return false;
        }
      }

      return true;
    });
  }, [data, filters]);

  // Helper function to convert 12-hour time to 24-hour format
  const convertTo24Hour = (time12h: string): string => {
    const [time, modifier] = time12h.split(" ");
    let [hours] = time.split(":");
    const [, minutes] = time.split(":");

    if (hours === "12") {
      hours = "00";
    }

    if (modifier === "PM") {
      hours = String(parseInt(hours, 10) + 12);
    }

    return `${hours.padStart(2, "0")}:${minutes}`;
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  return (
    <div className="flex flex-col h-screen w-6xl mx-auto py-8">
      {/* <ModeToggle /> */}
      <div className="flex flex-col mb-4">
        <div className="text-2xl font-semibold">Dance Class Schedule</div>
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
      <div className="flex-1 overflow-auto min-h-0">
        <DataTable columns={columns} data={filteredData} loading={loading} />
      </div>
      {totalPages > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
          disabled={loading}
        />
      )}
    </div>
  );
}
