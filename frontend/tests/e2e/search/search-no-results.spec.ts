import { expect, Page, test } from "@playwright/test";
import { BrowserContextOptions } from "playwright-core";

import {
  expectURLContainsQueryParam,
  fillSearchInputAndSubmit,
  generateRandomString,
} from "./searchSpecUtil";

interface PageProps {
  page: Page;
  browserName?: string;
  contextOptions?: BrowserContextOptions;
}

test.describe("Search page tests", () => {
  test("should return 0 results when searching for obscure term", async ({
    page,
  }: PageProps) => {
    await page.goto("/search");

    const searchTerm = generateRandomString([10]);

    await fillSearchInputAndSubmit(searchTerm, page);
    await new Promise((resolve) => setTimeout(resolve, 3250));
    expectURLContainsQueryParam(page, "query", searchTerm);

    // eslint-disable-next-line testing-library/prefer-screen-queries
    const resultsHeading = page.getByRole("heading", {
      name: /0 Opportunities/i,
    });
    await expect(resultsHeading).toBeVisible();

    await expect(page.locator("div.usa-prose h2")).toHaveText(
      "Your search did not return any results.",
    );
  });
});
