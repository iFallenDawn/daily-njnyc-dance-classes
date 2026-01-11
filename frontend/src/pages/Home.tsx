"use client";

// react
import { useEffect, useState, useMemo } from "react";

// data table stuff
import { columns } from "../components/class-table/columns";
import { DataTable } from "../components/class-table/data-table";

// api
import { get_all_classes, type DanceClass } from "@/api/index";

// utils
import { formatDate, formatTime } from "@/lib/formatting";
import { parse } from "date-fns";

// custom components
// import { ModeToggle } from "@/components/mode-toggle";
import SearchBar, {
  type FilterState,
} from "@/components/class-table/search-bar";

export default function Home() {
  const [data, setData] = useState<DanceClass[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Extract unique studios and instructors from data
  const studios = useMemo(() => {
    const uniqueStudios = Array.from(new Set(data.map((d) => d.studio)));
    return uniqueStudios.sort();
  }, [data]);

  const instructors = useMemo(() => {
    const uniqueInstructors = Array.from(
      new Set(data.map((d) => d.instructor))
    );
    return uniqueInstructors.sort();
  }, [data]);

  // Initialize filters with all studios and instructors selected
  const [filters, setFilters] = useState<FilterState>({
    title: "",
    studios: new Set<string>(),
    instructors: new Set<string>(),
    startDate: undefined,
    endDate: undefined,
    startTime: undefined,
    endTime: undefined,
  });

  // Update filters when data changes to select all studios and instructors
  useEffect(() => {
    if (studios.length > 0 && filters.studios.size === 0) {
      setFilters((prev) => ({
        ...prev,
        studios: new Set(studios),
      }));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studios]);

  useEffect(() => {
    if (instructors.length > 0 && filters.instructors.size === 0) {
      setFilters((prev) => ({
        ...prev,
        instructors: new Set(instructors),
      }));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [instructors]);

  useEffect(() => {
    let isMounted = true;

    const fetchClasses = async () => {
      try {
        setLoading(true);
        setError(null);
        const classes = await get_all_classes({
          page: 1,
          limit: 50,
        });

        // format class dates and times
        classes.forEach((danceClass) => {
          danceClass.date = formatDate(danceClass.start_time);
          danceClass.start_time = formatTime(danceClass.start_time);
          danceClass.end_time = formatTime(danceClass.end_time);
        });

        if (isMounted) {
          setData(classes);
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
  }, []);

  // Apply all filters
  const filteredData = useMemo(() => {
    return data.filter((danceClass) => {
      // Title filter
      if (
        filters.title &&
        !danceClass.title.toLowerCase().includes(filters.title.toLowerCase())
      ) {
        return false;
      }

      // Studio filter - if no studios selected, show no results
      if (studios.length > 0 && !filters.studios.has(danceClass.studio)) {
        return false;
      }

      // Instructor filter - if no instructors selected, show no results
      if (
        instructors.length > 0 &&
        !filters.instructors.has(danceClass.instructor)
      ) {
        return false;
      }

      // Date range filter
      if (filters.startDate || filters.endDate) {
        try {
          const classDate = parse(danceClass.date, "MMM dd, yyyy", new Date());

          if (filters.startDate && classDate < filters.startDate) {
            return false;
          }

          if (filters.endDate && classDate > filters.endDate) {
            return false;
          }
        } catch {
          // If date parsing fails, exclude the class
          return false;
        }
      }

      // Time range filter - check if class time overlaps with selected range
      if (filters.startTime || filters.endTime) {
        try {
          const classStart24 = convertTo24Hour(danceClass.start_time);
          const classEnd24 = convertTo24Hour(danceClass.end_time);

          // Check if class overlaps with the filter range
          // Class should start before or at filter end time, and end after or at filter start time
          if (filters.startTime && classEnd24 < filters.startTime) {
            return false;
          }

          if (filters.endTime && classStart24 > filters.endTime) {
            return false;
          }
        } catch {
          // If time parsing fails, exclude the class
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

  return (
    <div className="flex flex-col w-6xl mx-auto my-8">
      {/* <ModeToggle /> */}
      <div className="flex flex-col">
        <div className="text-2xl font-semibold">Dance Class Schedule</div>
        <div className="text-muted-foreground">
          Browse and filter dance classes
        </div>
      </div>
      <SearchBar
        studios={studios}
        instructors={instructors}
        filters={filters}
        onFiltersChange={setFilters}
      />
      {error && <div className="text-red-500 mb-4">Error: {error}</div>}
      {loading ? (
        <div className="text-center py-8">Loading classes...</div>
      ) : (
        <DataTable columns={columns} data={filteredData} />
      )}
    </div>
  );
}
