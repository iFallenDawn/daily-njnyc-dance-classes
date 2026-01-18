import { useState, useMemo } from "react";
import { ListFilter } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";

interface InstructorFilterProps {
  instructors: string[];
  selectedInstructors: Set<string>;
  onInstructorsChange: (instructors: Set<string>) => void;
}

export function InstructorFilter({
  instructors,
  selectedInstructors,
  onInstructorsChange,
}: InstructorFilterProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const filteredInstructors = useMemo(() => {
    if (!searchQuery.trim()) return instructors;
    return instructors.filter((instructor) =>
      instructor.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [instructors, searchQuery]);

  const handleSelectAll = () => {
    onInstructorsChange(new Set(instructors));
  };

  const handleClearAll = () => {
    onInstructorsChange(new Set());
  };

  const handleToggleInstructor = (instructor: string) => {
    const newSelected = new Set(selectedInstructors);
    if (newSelected.has(instructor)) {
      newSelected.delete(instructor);
    } else {
      newSelected.add(instructor);
    }
    onInstructorsChange(newSelected);
  };

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-full">
          <ListFilter /> Instructor
          {selectedInstructors.size > 0 &&
            selectedInstructors.size < instructors.length && (
              <span className="ml-1 text-xs">({selectedInstructors.size})</span>
            )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0" align="start">
        <div className="p-4 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="font-semibold text-sm">Filter by Instructor</h4>
            <span className="text-xs text-muted-foreground">
              {selectedInstructors.size} / {instructors.length} selected
            </span>
          </div>

          <Input
            placeholder="Search instructors..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="h-9"
          />

          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleSelectAll}
              className="flex-1 h-8 text-xs"
            >
              Select All
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleClearAll}
              className="flex-1 h-8 text-xs"
            >
              Clear All
            </Button>
          </div>

          <Separator />

          <div className="max-h-64 overflow-y-auto space-y-2">
            {filteredInstructors.length > 0 ? (
              filteredInstructors.map((instructor) => (
                <div
                  key={instructor}
                  className="flex items-center space-x-2 p-2 rounded-sm"
                >
                  <Checkbox
                    id={`instructor-${instructor}`}
                    checked={selectedInstructors.has(instructor)}
                    onCheckedChange={() => handleToggleInstructor(instructor)}
                  />
                  <label
                    htmlFor={`instructor-${instructor}`}
                    className="text-sm flex-1"
                  >
                    {instructor}
                  </label>
                </div>
              ))
            ) : (
              <div className="text-sm text-muted-foreground text-center py-4">
                No instructors found
              </div>
            )}
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
