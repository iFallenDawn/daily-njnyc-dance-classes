"use client"

import type { ColumnDef } from "@tanstack/react-table"
import type { DanceClass } from "@/api/index"

export const columns: ColumnDef<DanceClass>[] = [
  {
    accessorKey: "title",
    header: "Class",
  },
  {
    accessorKey: "instructor",
    header: "Instructor",
  },
  {
    accessorKey: "studio",
    header: "Studio",
  },
  {
    accessorKey: "style",
    header: "Style",
  },
  {
    accessorKey: "date",
    header: "Date",
  },
  {
    accessorKey: "start_time",
    header: "Start Time",
  },
  {
    accessorKey: "end_time",
    header: "End Time",
  },
  {
    accessorKey: "difficulty",
    header: "Difficulty",
  },
]