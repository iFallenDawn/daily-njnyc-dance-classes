// format datetime string into date
export const formatDate = (datetimeStr: string): string => {
  const date = new Date(datetimeStr);
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

// format datetime string into time
export const formatTime = (datetimeStr: string): string => {
  const date = new Date(datetimeStr);
  return date.toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  });
};
