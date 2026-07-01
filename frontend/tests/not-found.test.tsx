import { render, screen } from "@testing-library/react";

jest.mock("next/link", () => {
  return function MockLink({ children, href }: { children: React.ReactNode; href: string }) {
    return <a href={href}>{children}</a>;
  };
});

import NotFound from "@/app/not-found";

describe("404 Not Found Page", () => {
  it("displays 404 heading", () => {
    render(<NotFound />);
    expect(screen.getByText("404")).toBeInTheDocument();
  });

  it("displays Page Not Found message", () => {
    render(<NotFound />);
    expect(screen.getByText("Page Not Found")).toBeInTheDocument();
  });

  it("has a link to the dashboard", () => {
    render(<NotFound />);
    const dashboardLink = screen.getByRole("link", { name: /go to dashboard/i });
    expect(dashboardLink).toHaveAttribute("href", "/dashboard");
  });

  it("has a link to the home page", () => {
    render(<NotFound />);
    const homeLink = screen.getByRole("link", { name: /home/i });
    expect(homeLink).toHaveAttribute("href", "/");
  });
});
