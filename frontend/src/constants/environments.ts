const {
  NODE_ENV,
  NEXT_PUBLIC_BASE_PATH,
  USE_SEARCH_MOCK_DATA = "",
  SENDY_API_URL,
  SENDY_API_KEY,
  SENDY_LIST_ID,
  API_URL,
  API_AUTH_TOKEN = "",
  NEXT_PUBLIC_BASE_URL,
  // NEXT_PUBLIC_BUILD_TIME = "",
  // NEXT_PUBLIC_RUN_TIME = "",
} = process.env;

// console.log("!! destructured build time", NEXT_PUBLIC_BUILD_TIME);
// console.log("!! destructured run time", NEXT_PUBLIC_RUN_TIME);
console.log("!! inline build time", process.env.NEXT_PUBLIC_BUILD_TIME);
console.log("!! inline run time", process.env.NEXT_PUBLIC_RUN_TIME);

// home for all interpreted server side environment variables
export const environment: { [key: string]: string } = {
  LEGACY_HOST:
    NODE_ENV === "production"
      ? "https://grants.gov"
      : "https://test.grants.gov",
  NEXT_PUBLIC_BASE_PATH: NEXT_PUBLIC_BASE_PATH ?? "",
  USE_SEARCH_MOCK_DATA,
  SENDY_API_URL: SENDY_API_URL || "",
  SENDY_API_KEY: SENDY_API_KEY || "",
  SENDY_LIST_ID: SENDY_LIST_ID || "",
  API_URL: API_URL || "",
  API_AUTH_TOKEN,
  NEXT_PUBLIC_BASE_URL: NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  GOOGLE_TAG_MANAGER_ID: "GTM-MV57HMHS",
  NEXT_PUBLIC_BUILD_TIME: process.env.NEXT_PUBLIC_BUILD_TIME || "",
  NEXT_PUBLIC_RUN_TIME: process.env.NEXT_PUBLIC_RUN_TIME || "",
};
