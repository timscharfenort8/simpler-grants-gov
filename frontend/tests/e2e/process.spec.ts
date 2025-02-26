/* eslint-disable testing-library/prefer-screen-queries */
import { expect, test } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.goto("/process");
});

test.afterEach(async ({ context }) => {
  await context.close();
});

test("has title", async ({ page }) => {
  await expect(page).toHaveTitle("Process | Simpler.Grants.gov");
});

test("can view banner and return to top after scrolling to the bottom", async ({
  page,
}, {
  project: {
    use: { isMobile, defaultBrowserType },
  },
}) => {
  const isMobileSafari = isMobile && defaultBrowserType === "webkit";
  const returnToTopLink = page.getByRole("link", { name: /return to top/i });

  // https://github.com/microsoft/playwright/issues/2179
  if (!isMobileSafari) {
    await returnToTopLink.scrollIntoViewIfNeeded();
  } else {
    await page.evaluate(() =>
      window.scrollTo(0, document.documentElement.scrollHeight),
    );
  }

  await expect(
    page.getByRole("heading", {
      name: /This site is a work in progress, with new features and updates based on your feedback./i,
    }),
  ).toBeVisible();

  await returnToTopLink.click();

  await expect(returnToTopLink).not.toBeInViewport();
  await expect(
    page.getByRole("heading", { name: "Our open process" }),
  ).toBeInViewport();
});

test("can view the API milestone on GitHub", async ({ page }) => {
  await page
    .getByRole("link", { name: "View the API milestone on GitHub" })
    .click();

  await expect(page).toHaveURL(
    /https:\/\/github.com\/HHS\/simpler-grants-gov\/issues\/70/,
  );
});

test("can view the search milestone on GitHub", async ({ page }) => {
  await page
    .getByRole("link", { name: "View the search milestone on GitHub" })
    .click();

  await expect(page).toHaveURL(
    /https:\/\/github.com\/HHS\/simpler-grants-gov\/issues\/89/,
  );
});
