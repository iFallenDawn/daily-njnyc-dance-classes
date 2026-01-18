import { useState } from "react";
import { Calendar as CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";
import type { DateRange } from "react-day-picker";

interface DateRangeFilterProps {
  startDate: Date | undefined;
  endDate: Date | undefined;
  onDateRangeChange: (
    startDate: Date | undefined,
    endDate: Date | undefined
  ) => void;
}

export function DateRangeFilter({
  startDate,
  endDate,
  onDateRangeChange,
}: DateRangeFilterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [dateRange, setDateRange] = useState<DateRange | undefined>({
    from: startDate,
    to: endDate,
  });

  const handleClear = () => {
    setDateRange(undefined);
    onDateRangeChange(undefined, undefined);
  };

  const handleApply = () => {
    onDateRangeChange(dateRange?.from, dateRange?.to);
    setIsOpen(false);
  };

  const hasSelection = startDate || endDate;

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-full justify-start">
          <CalendarIcon className="h-4 w-4" />
          {hasSelection ? (
            <span className="truncate">
              {startDate ? format(startDate, "MMM dd") : "Start"} -{" "}
              {endDate ? format(endDate, "MMM dd") : "End"}
            </span>
          ) : (
            "Date range"
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        <div className="p-4 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="font-semibold text-sm">Select Date Range</h4>
          </div>

          <Calendar
            mode="range"
            selected={dateRange}
            onSelect={setDateRange}
            initialFocus
            numberOfMonths={2}
          />

          <Separator />

          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleClear}
              className="flex-1"
            >
              Clear
            </Button>
            <Button size="sm" onClick={handleApply} className="flex-1">
              Apply
            </Button>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
