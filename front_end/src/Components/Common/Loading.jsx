export default function Loading({ children = "Loading..." }) {
  return (
    <p className="govuk-body" style={{ textAlign: "center", fontSize: "2rem" }}>
      {children}
    </p>
  );
}
