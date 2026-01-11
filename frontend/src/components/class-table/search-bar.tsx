"use client"

// form stuff
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

// lucide icons
import { Calendar, Clock, ListFilter } from 'lucide-react';

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
})

type SearchFormValues = z.infer<typeof searchSchema>

// shadcn components
import { Button } from "@/components/ui/button"
import {
  Field, FieldDescription,
  FieldGroup,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

export default function SearchBar() {
  return <div>
    <form className="flex flex-col gap-2 mb-4 md:flex-row">
      <Field className="w-full md:w-1/2">
        <Input placeholder="Search class names..." />
      </Field>
      <div className="flex flex-col gap-2 w-full md:w-1/2 md:flex-row">
        <Field className="w-full md:w-1/4">
          <Button variant="outline" className="w-full"><ListFilter /> Studio</Button>
        </Field>
        <Field className="w-full md:w-1/4">
          <Button variant="outline" className="w-full"><ListFilter /> Instructor</Button>
        </Field>
        <Field className="w-full md:w-1/4">
          <Button variant="outline" className="w-full"><Calendar /> Date range</Button>
        </Field>
        <Field className="w-full md:w-1/4">
          <Button variant="outline" className="w-full"><Clock /> Time range</Button>
        </Field>
      </div>
    </form>
  </div>
}