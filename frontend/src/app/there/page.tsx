
import { unstable_setRequestLocale } from "next-intl/server";
import { useTranslations } from "next-intl";


export default function Here({ params }: { params: { locale: string } }) {
  const { locale } = params;
  unstable_setRequestLocale(locale);
  // await new Promise((resolve) => setTimeout(resolve, 1250))
  const t = useTranslations();
  if (t.name) {
    console.log("wtf")
  }

  return (
    <>
      <h1>there</h1>
    </>
  );
}
