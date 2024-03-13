import {
  ServerSideRouteParams,
  ServerSideSearchParams,
} from "../../types/requestURLTypes";

import { FeatureFlagsManager } from "../../services/FeatureFlagManager";
import PageSEO from "src/components/PageSEO";
import React from "react";
import SearchCallToAction from "../../components/search/SearchCallToAction";
import { SearchForm } from "./SearchForm";
import { cookies } from "next/headers";
import { forceSearchParamsToStringValue } from "../../utils/convertSearchParamsToStrings";
import { getSearchFetcher } from "../../services/searchfetcher/SearchFetcherUtil";
import { notFound } from "next/navigation";

const searchFetcher = getSearchFetcher();

// TODO: use for i18n when ready
// interface RouteParams {
//   locale: string;
// }

interface ServerPageProps {
  params: ServerSideRouteParams;
  searchParams: ServerSideSearchParams;
}

export default async function Search({ searchParams }: ServerPageProps) {
  console.log("searchParams serer side =>", searchParams);

  const ffManager = new FeatureFlagsManager(cookies());
  if (!ffManager.isFeatureEnabled("showSearchV0")) {
    return notFound();
  }

  const convertedSearchParams = forceSearchParamsToStringValue(searchParams);
  const initialSearchResults = await searchFetcher.fetchOpportunities();

  return (
    <>
      {/* TODO: i18n */}
      <PageSEO
        title="Search Funding Opportunities"
        description="Try out our experimental search page."
      />
      <SearchCallToAction />
      <SearchForm
        initialSearchResults={initialSearchResults}
        requestURLQueryParams={convertedSearchParams}
      />
    </>
  );
}
