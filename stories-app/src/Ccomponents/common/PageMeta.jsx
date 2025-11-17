// import { HelmetProvider, Helmet } from "react-helmet-async";

const PageMeta = ({
  title,
  description,
}) => (
  <div>
    <title>{title}</title>
    <meta name="description" content={description} />
  </div>
);

export const AppWrapper = ({ children }) => (
  <div>{children}</div>
);

export default PageMeta;
