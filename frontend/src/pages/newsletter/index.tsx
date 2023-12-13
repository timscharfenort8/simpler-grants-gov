import type { GetStaticProps, NextPage } from "next";
import { NEWSLETTER_CRUMBS } from "src/constants/breadcrumbs";

import { Trans, useTranslation } from "next-i18next";
import { serverSideTranslations } from "next-i18next/serverSideTranslations";
import { useState } from "react";
import {
  Button,
  Grid,
  GridContainer,
  Label,
  TextInput,
} from "@trussworks/react-uswds";

import Breadcrumbs from "src/components/Breadcrumbs";
import PageSEO from "src/components/PageSEO";
import BetaAlert from "../../components/BetaAlert";

const Newsletter: NextPage = () => {
  const { t } = useTranslation("common", { keyPrefix: "Newsletter" });

  const [formData, setFormData] = useState({
    name: "",
    LastName: "",
    email: "",
    list: "A2zerhEC59Ea6mzTgzdTgw",
    subform: "yes",
    hp: "",
  });

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const fieldName = e.target.name;
    const fieldValue = e.target.value;

    setFormData((prevState) => ({
      ...prevState,
      [fieldName]: fieldValue,
    }));
  };

  return (
    <>
      <PageSEO title={t("page_title")} description={t("meta_description")} />
      <BetaAlert />
      <Breadcrumbs breadcrumbList={NEWSLETTER_CRUMBS} />

      <GridContainer className="padding-bottom-5 tablet:padding-top-0 desktop-lg:padding-top-0 border-bottom-2px border-base-lightest">
        <h1 className="margin-0 tablet-lg:font-sans-xl desktop-lg:font-sans-2xl">
          {t("title")}
        </h1>
        <p className="usa-intro font-sans-md tablet:font-sans-lg desktop-lg:font-sans-xl margin-bottom-0">
          {t("intro")}
        </p>
        <Grid row gap className="flex-align-start">
          <Grid tabletLg={{ col: 6 }}>
            <p className="usa-intro">{t("paragraph_1")}</p>
            <Trans
              t={t}
              i18nKey="list"
              components={{
                ul: (
                  <ul className="usa-list margin-top-0 tablet-lg:margin-top-3 font-sans-md line-height-sans-4" />
                ),
                li: <li />,
              }}
            />
          </Grid>
          <Grid tabletLg={{ col: 6 }}>
            <form
              data-testid="sendy-form"
              action="https://communications.grants.gov/app/subscribe"
              method="POST"
              acceptCharset="utf-8"
            >
              <Label htmlFor="name">
                First Name{" "}
                <span title="required" className="usa-hint usa-hint--required ">
                  (required)
                </span>
              </Label>
              <TextInput
                aria-required
                type="text"
                name="name"
                id="name"
                value={formData.name}
                required
                onChange={handleInput}
              />
              <Label htmlFor="LastName" hint=" (optional)">
                Last Name
              </Label>
              <TextInput
                type="text"
                name="LastName"
                id="LastName"
                value={formData.LastName}
                onChange={handleInput}
              />
              <Label htmlFor="email">
                Email{" "}
                <span title="required" className="usa-hint usa-hint--required ">
                  (required)
                </span>
              </Label>
              <TextInput
                aria-required
                type="email"
                name="email"
                id="email"
                required
                value={formData.email}
                onChange={handleInput}
              />
              <div className="display-none">
                <Label htmlFor="hp">HP</Label>
                <TextInput
                  type="text"
                  name="hp"
                  id="hp"
                  value={formData.hp}
                  onChange={handleInput}
                />
              </div>
              <input type="hidden" name="list" value="A2zerhEC59Ea6mzTgzdTgw" />
              <input type="hidden" name="subform" value="yes" />
              <Button
                type="submit"
                name="submit"
                id="submit"
                className="margin-top-4"
              >
                Subscribe
              </Button>
            </form>
          </Grid>
        </Grid>
      </GridContainer>
      <GridContainer className="padding-bottom-5 tablet:padding-top-3 desktop-lg:padding-top-3">
        <p className="font-sans-3xs text-base-dark">{t("disclaimer")}</p>
      </GridContainer>
    </>
  );
};

// Change this to GetServerSideProps if you're using server-side rendering
export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale ?? "en");
  return { props: { ...translations } };
};

export default Newsletter;