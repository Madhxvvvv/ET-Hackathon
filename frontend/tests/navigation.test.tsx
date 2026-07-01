import { render, screen } from "@testing-library/react";

jest.mock("next/link", () => {
  return function MockLink({ children, href, "aria-label": ariaLabel, ...rest }: { children: React.ReactNode; href: string; "aria-label"?: string; [key: string]: unknown }) {
    return <a href={href} aria-label={ariaLabel} {...rest}>{children}</a>;
  };
});

jest.mock("next/navigation", () => ({
  usePathname: () => "/scanner",
}));

import { Breadcrumb } from "@/components/layout/Breadcrumb";

describe("Breadcrumb", () => {
  it("renders nav landmark with label", () => {
    render(<Breadcrumb items={[{ label: "Currency Scanner" }]} />);
    expect(screen.getByRole("navigation", { name: /breadcrumb/i })).toBeInTheDocument();
  });

  it("renders all items", () => {
    render(
      <Breadcrumb
        items={[
          { label: "Dashboard", href: "/dashboard" },
          { label: "Scanner" },
        ]}
      />
    );
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Scanner")).toBeInTheDocument();
  });

  it("renders home link pointing to /", () => {
    render(<Breadcrumb items={[{ label: "Test" }]} />);
    const homeLink = screen.getByRole("link", { name: /home/i });
    expect(homeLink).toHaveAttribute("href", "/");
  });

  it("marks last item as current page", () => {
    render(
      <Breadcrumb items={[{ label: "Dashboard", href: "/dashboard" }, { label: "Scanner" }]} />
    );
    expect(screen.getByText("Scanner")).toHaveAttribute("aria-current", "page");
  });
});
