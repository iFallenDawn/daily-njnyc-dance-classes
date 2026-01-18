import { useState } from "react";
import { Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";

interface TimeRangeFilterProps {
  startTime: string | undefined;
  endTime: string | undefined;
  onTimeRangeChange: (
    startTime: string | undefined,
    endTime: string | undefined
  ) => void;
}

export function TimeRangeFilter({
  startTime,
  endTime,
  onTimeRangeChange,
}: TimeRangeFilterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [tempStartTime, setTempStartTime] = useState<string>(startTime || "");
  const [tempEndTime, setTempEndTime] = useState<string>(endTime || "");

  const handleClear = () => {
    setTempStartTime("");
    setTempEndTime("");
    onTimeRangeChange(undefined, undefined);
  };

  const handleApply = () => {
    onTimeRangeChange(tempStartTime || undefined, tempEndTime || undefined);
    setIsOpen(false);
  };

  const hasSelection = startTime || endTime;

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-full justify-start">
          <Clock className="h-4 w-4" />
          {hasSelection ? (
            <span className="truncate">
              {startTime || "Start"} - {endTime || "End"}
            </span>
          ) : (
            "Time range"
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0" align="start">
        <div className="p-4 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="font-semibold text-sm">Select Time Range</h4>
          </div>

          <div className="space-y-3">
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">
                Start Time
              </label>
              <Input
                type="time"
                value={tempStartTime}
                onChange={(e) => setTempStartTime(e.target.value)}
                className="h-9"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">End Time</label>
              <Input
                type="time"
                value={tempEndTime}
                onChange={(e) => setTempEndTime(e.target.value)}
                className="h-9"
              />
            </div>
          </div>

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
