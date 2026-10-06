"use client";

import type { ColumnDef } from "@tanstack/react-table";

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { DanceClass } from "@/api/index";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  loading: boolean;
}

export function DataTable<TData, TValue>({
  columns,
  data,
  loading,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (loading) {
    return (
      <div
        className="flex items-center justify-center rounded-md border bg-background"
        style={{ height: "400px" }}
      >
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
          <span className="text-muted-foreground">Loading classes...</span>
        </div>
      </div>
    );
  }

  return (
    <>
      {/* phones: one card per class */}
      <div className="flex flex-col gap-2 md:hidden">
        {data.length ? (
          (data as DanceClass[]).map((danceClass, index) => (
            <div key={index} className="rounded-md border bg-background p-4">
              <div className="font-medium">{danceClass.title}</div>
              <div className="text-sm text-muted-foreground">
                {danceClass.studio} · {danceClass.instructor}
              </div>
              <div className="mt-1 text-sm">
                {danceClass.date}, {danceClass.start_time} – {danceClass.end_time}
              </div>
              {danceClass.difficulty && (
                <div className="text-sm text-muted-foreground">
                  {danceClass.difficulty}
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="rounded-md border bg-background p-6 text-center">
            No results.
          </div>
        )}
      </div>
      {/* desktop: table */}
      <div className="hidden overflow-hidden rounded-md border md:block">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <TableHead key={header.id} className="p-4">
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                );
              })}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
                className="bg-background"
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id} className="p-4">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
      </div>
    </>
  );
}
