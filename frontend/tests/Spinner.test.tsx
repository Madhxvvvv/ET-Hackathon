import { render, screen } from "@testing-library/react";
import { Spinner, PageSpinner } from "@/components/ui/Spinner";

describe("Spinner", () => {
  it("has status role", () => {
    render(<Spinner />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("renders custom label in sr-only span", () => {
    render(<Spinner label="Uploading" />);
    expect(screen.getByText("Uploading")).toBeInTheDocument();
  });
});

describe("PageSpinner", () => {
  it("renders a centered loading indicator", () => {
    render(<PageSpinner />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });
});
