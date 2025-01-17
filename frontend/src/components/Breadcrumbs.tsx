import {
  Breadcrumb,
  BreadcrumbBar,
  BreadcrumbLink,
  GridContainer,
} from "@trussworks/react-uswds";

export type Breadcrumb = {
  title: string;
  path: string;
};

export type BreadcrumbList = Breadcrumb[];

type Props = {
  breadcrumbList: BreadcrumbList;
};

const rdfaMetadata = {
  ol: {
    vocab: "http://schema.org/",
    typeof: "BreadcrumbList",
  },
  li: {
    property: "itemListElement",
    typeof: "ListItem",
  },
  a: {
    property: "item",
    typeof: "WebPage",
  },
};

const Breadcrumbs = ({ breadcrumbList }: Props) => {
  const breadcrumArray = breadcrumbList.map((breadcrumbInfo, i) => {
    return (
      <Breadcrumb
        key={breadcrumbInfo.title + "-crumb"}
        current={i + 1 === breadcrumbList.length}
        {...rdfaMetadata.li}
      >
        {i + 1 !== breadcrumbList.length ? (
          <BreadcrumbLink href={breadcrumbInfo.path} {...rdfaMetadata.a}>
            {}
            <span property="name">{breadcrumbInfo.title}</span>
          </BreadcrumbLink>
        ) : (
          <span property="name">{breadcrumbInfo.title}</span>
        )}
        <meta property="position" content={(i + 1).toString()} />
      </Breadcrumb>
    );
  });

  return (
    <GridContainer
      className="padding-top-1 tablet:padding-top-3 desktop-lg:padding-top-4"
      data-testid="breadcrumb"
    >
      <BreadcrumbBar listProps={{ ...rdfaMetadata.ol }}>
        {breadcrumArray}
      </BreadcrumbBar>
    </GridContainer>
  );
};

export default Breadcrumbs;
