"use client";

import React from "react";

// form stuff
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

// Validation schema
const searchSchema = z.object({
  title: z.string().optional(),
  instructor: z.string().optional(),
  studios: z.array(z.string()).optional(),
  style: z.string().optional(),
  date: z.string().optional(),
  start_time: z.string().optional(),
  end_time: z.string().optional(),
  difficulty: z.string().optional(),
  cancelled: z.boolean().optional(),
});

type SearchFormValues = z.infer<typeof searchSchema>;

export interface FilterState {
  title: string;
  studios: Set<string>;
  instructors: Set<string>;
  startDate: Date | undefined;
  endDate: Date | undefined;
  startTime: string | undefined;
  endTime: string | undefined;
}

interface SearchBarProps {
  studios: string[];
  instructors: string[];
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
}

// shadcn components
import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";

// filter components
import { StudioFilter } from "./studio-filter";
import { InstructorFilter } from "./instructor-filter";
import { DateRangeFilter } from "./date-range-filter";
import { TimeRangeFilter } from "./time-range-filter";

export default function SearchBar({
  studios,
  instructors,
  filters,
  onFiltersChange,
}: SearchBarProps) {
  const { register, watch } = useForm<SearchFormValues>({
    resolver: zodResolver(searchSchema),
    defaultValues: {
      title: "",
    },
  });

  // watch the title field and trigger search on change
  const titleValue = watch("title");

  // trigger search whenever title changes
  React.useEffect(() => {
    onFiltersChange({ ...filters, title: titleValue || "" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [titleValue]);

  return (
    <div className="bg-background p-4 my-4 rounded-md shadow-sm border border-border">
      <form className="flex flex-col gap-2 md:flex-row">
        <Field className="w-full md:w-1/2">
          <Input placeholder="Search class names..." {...register("title")} />
        </Field>
        <div className="flex flex-col gap-2 w-full md:w-1/2 md:flex-row">
          <Field className="w-full md:w-1/4">
            <StudioFilter
              studios={studios}
              selectedStudios={filters.studios}
              onStudiosChange={(studios) =>
                onFiltersChange({ ...filters, studios })
              }
            />
          </Field>
          <Field className="w-full md:w-1/4">
            <InstructorFilter
              instructors={instructors}
              selectedInstructors={filters.instructors}
              onInstructorsChange={(instructors) =>
                onFiltersChange({ ...filters, instructors })
              }
            />
          </Field>
          <Field className="w-full md:w-1/4">
            <DateRangeFilter
              startDate={filters.startDate}
              endDate={filters.endDate}
              onDateRangeChange={(startDate, endDate) =>
                onFiltersChange({ ...filters, startDate, endDate })
              }
            />
          </Field>
          <Field className="w-full md:w-1/4">
            <TimeRangeFilter
              startTime={filters.startTime}
              endTime={filters.endTime}
              onTimeRangeChange={(startTime, endTime) =>
                onFiltersChange({ ...filters, startTime, endTime })
              }
            />
          </Field>
        </div>
      </form>
    </div>
  );
}
