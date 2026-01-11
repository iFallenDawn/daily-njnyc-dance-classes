"use client"

// react
import { useEffect, useState } from "react"

// data table stuff
import { columns } from "../components/class-table/columns"
import { DataTable } from "../components/class-table/data-table"

// api
import { get_all_classes, type DanceClass } from "@/api/index"

// custom components
import SearchBar from "@/components/class-table/search-bar"

export default function Home() {
  const [data, setData] = useState<DanceClass[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let isMounted = true

    const fetchClasses = async () => {
      try {
        setLoading(true)
        setError(null)
        const classes = await get_all_classes({
          page: 1,
          limit: 50,
        })
        if (isMounted) {
          setData(classes)
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Failed to fetch classes')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchClasses()

    return () => {
      isMounted = false
    }
  }, [])

  return <div className="flex flex-col">
    <div>Dance Class Schedule</div>
    <div>Browse and filter dance classes</div>
    <SearchBar />
    {error && <div className="text-red-500 mb-4">Error: {error}</div>}
    {loading ? (
      <div className="text-center py-8">Loading classes...</div>
    ) : (
      <DataTable columns={columns} data={data} />
    )}
  </div>
}

