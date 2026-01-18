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

interface StudioFilterProps {
  studios: string[];
  selectedStudios: Set<string>;
  onStudiosChange: (studios: Set<string>) => void;
}

export function StudioFilter({
  studios,
  selectedStudios,
  onStudiosChange,
}: StudioFilterProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const filteredStudios = useMemo(() => {
    if (!searchQuery.trim()) return studios;
    return studios.filter((studio) =>
      studio.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [studios, searchQuery]);

  const handleSelectAll = () => {
    onStudiosChange(new Set(studios));
  };

  const handleClearAll = () => {
    onStudiosChange(new Set());
  };

  const handleToggleStudio = (studio: string) => {
    const newSelected = new Set(selectedStudios);
    if (newSelected.has(studio)) {
      newSelected.delete(studio);
    } else {
      newSelected.add(studio);
    }
    onStudiosChange(newSelected);
  };

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-full">
          <ListFilter /> Studio
          {selectedStudios.size > 0 &&
            selectedStudios.size < studios.length && (
              <span className="ml-1 text-xs">({selectedStudios.size})</span>
            )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0" align="start">
        <div className="p-4 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="font-semibold text-sm">Filter by Studio</h4>
            <span className="text-xs text-muted-foreground">
              {selectedStudios.size} / {studios.length} selected
            </span>
          </div>

          <Input
            placeholder="Search studios..."
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
            {filteredStudios.length > 0 ? (
              filteredStudios.map((studio) => (
                <div
                  key={studio}
                  className="flex items-center space-x-2 p-2 rounded-sm"
                >
                  <Checkbox
                    id={`studio-${studio}`}
                    checked={selectedStudios.has(studio)}
                    onCheckedChange={() => handleToggleStudio(studio)}
                  />
                  <label
                    htmlFor={`studio-${studio}`}
                    className="text-sm flex-1"
                  >
                    {studio}
                  </label>
                </div>
              ))
            ) : (
              <div className="text-sm text-muted-foreground text-center py-4">
                No studios found
              </div>
            )}
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
