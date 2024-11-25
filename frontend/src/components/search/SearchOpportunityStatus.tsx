"use client";

import { QueryContext } from "src/app/[locale]/search/QueryProvider";
import { environment } from "src/constants/environments";
import { SEARCH_NO_STATUS_VALUE } from "src/constants/search";
import { useSearchParamUpdater } from "src/hooks/useSearchParamUpdater";

import { useTranslations } from "next-intl";
import { useContext } from "react";
import { Checkbox } from "@trussworks/react-uswds";

interface StatusOption {
  id: string;
  label: string;
  value: string;
}

interface SearchOpportunityStatusProps {
  query: Set<string>;
  test: string;
}

export default function SearchOpportunityStatus({
  query,
  test,
}: SearchOpportunityStatusProps) {
  console.warn("!!! client component prop", test);
  console.warn(
    "!!! client side run imported",
    environment.NEXT_PUBLIC_RUN_TIME,
  );
  console.warn(
    "!!! client side BUILD imported",
    environment.NEXT_PUBLIC_BUILD_TIME,
  );
  console.warn("!!! client side run direct", process.env.NEXT_PUBLIC_RUN_TIME);
  console.warn(
    "!!! client side BUILD direct",
    process.env.NEXT_PUBLIC_BUILD_TIME,
  );
  const { queryTerm } = useContext(QueryContext);
  const { updateQueryParams } = useSearchParamUpdater();

  const handleCheck = (value: string, isChecked: boolean) => {
    const updated = new Set(query);
    isChecked ? updated.add(value) : updated.delete(value);
    // Add "status=NO_STATUS_VALUE" if no values are selected.
    if (updated.size === 0) {
      updated.add(SEARCH_NO_STATUS_VALUE);
    }
    updateQueryParams(updated, "status", queryTerm);
  };

  const t = useTranslations("Search");

  const statusOptions: StatusOption[] = [
    {
      id: "status-forecasted",
      label: t("opportunityStatus.label.forecasted"),
      value: "forecasted",
    },
    {
      id: "status-posted",
      label: t("opportunityStatus.label.posted"),
      value: "posted",
    },
    {
      id: "status-closed",
      label: t("opportunityStatus.label.closed"),
      value: "closed",
    },
    {
      id: "status-archived",
      label: t("opportunityStatus.label.archived"),
      value: "archived",
    },
  ];

  return (
    <>
      <h2 className="margin-bottom-1 font-sans-xs">
        {t("opportunityStatus.title")}
      </h2>
      <div className="grid-row flex-wrap">
        {statusOptions.map((option) => {
          return (
            <div key={option.id} className="grid-col-6 padding-right-1">
              <Checkbox
                id={option.id}
                name={option.id}
                label={option.label}
                tile={true}
                onChange={(e) => handleCheck(option.value, e.target.checked)}
                checked={query.has(option.value)}
              />
            </div>
          );
        })}
      </div>
    </>
  );
}
