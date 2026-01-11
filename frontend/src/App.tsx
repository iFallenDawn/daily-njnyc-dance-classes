"use client";

// theme provider
import { ThemeProvider } from "@/components/theme-provider";

// page
import Home from "@/pages/Home";

function App() {
  return (
    <>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <Home />
      </ThemeProvider>
    </>
  );
}

export default App;
