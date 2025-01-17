import "@testing-library/jest-dom";

import { fireEvent } from "@testing-library/react";
import { axe } from "jest-axe";
import QueryProvider from "src/app/[locale]/search/QueryProvider";
import { render, screen } from "tests/react-utils";

import { ReadonlyURLSearchParams } from "next/navigation";
import React from "react";

import SearchBar from "src/components/search/SearchBar";

// Mock the hook since it's used in the component
const mockUpdateQueryParams = jest.fn();

jest.mock("src/hooks/useSearchParamUpdater", () => ({
  useSearchParamUpdater: () => ({
    updateQueryParams: mockUpdateQueryParams,
    searchParams: new ReadonlyURLSearchParams(),
  }),
}));

describe("SearchBar", () => {
  const initialQueryParams = "initial query";

  it("should not have basic accessibility issues", async () => {
    const { container } = render(
      <QueryProvider>
        <SearchBar query={initialQueryParams} />
      </QueryProvider>,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("updates the input value when typing in the search field", () => {
    render(
      <QueryProvider>
        <SearchBar query={initialQueryParams} />
      </QueryProvider>,
    );

    const input = screen.getByRole("searchbox");
    fireEvent.change(input, { target: { value: "new query" } });

    expect(input).toHaveValue("new query");
  });

  it("calls updateQueryParams with the correct argument when submitting the form", () => {
    render(
      <QueryProvider>
        <SearchBar query={initialQueryParams} />
      </QueryProvider>,
    );

    const input = screen.getByRole("searchbox");
    fireEvent.change(input, { target: { value: "new query" } });

    const searchButton = screen.getByRole("button", { name: /search/i });
    fireEvent.click(searchButton);

    expect(mockUpdateQueryParams).toHaveBeenCalledWith(
      "",
      "query",
      "new query",
      false,
    );
  });
});
