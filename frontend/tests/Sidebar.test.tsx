import { render, screen, fireEvent } from "@testing-library/react";

// Mock next/navigation
jest.mock("next/navigation", () => ({
  usePathname: () => "/dashboard",
}));

// Mock next/link
jest.mock("next/link", () => {
  return function MockLink({ children, href, ...props }: { children: React.ReactNode; href: string; [key: string]: unknown }) {
    return <a href={href} {...props}>{children}</a>;
  };
});

import { Sidebar } from "@/components/layout/Sidebar";

describe("Sidebar", () => {
  const defaultProps = { isOpen: true, onClose: jest.fn() };

  it("renders navigation landmark", () => {
    render(<Sidebar {...defaultProps} />);
    expect(screen.getByRole("complementary", { name: /main navigation/i })).toBeInTheDocument();
  });

  it("renders all nav links", () => {
    render(<Sidebar {...defaultProps} />);
    expect(screen.getByRole("link", { name: /dashboard/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /currency scanner/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /fraud network/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /scam shield/i })).toBeInTheDocument();
  });

  it("marks active route with aria-current", () => {
    render(<Sidebar {...defaultProps} />);
    const dashboardLink = screen.getByRole("link", { name: /dashboard/i });
    expect(dashboardLink).toHaveAttribute("aria-current", "page");
  });

  it("calls onClose when close button is clicked", () => {
    const onClose = jest.fn();
    render(<Sidebar isOpen={true} onClose={onClose} />);
    const closeBtn = screen.getAllByRole("button", { name: /close sidebar/i })[0];
    fireEvent.click(closeBtn);
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("has correct href for each nav item", () => {
    render(<Sidebar {...defaultProps} />);
    const links = screen.getAllByRole("link");
    const hrefs = links.map((l) => l.getAttribute("href")).filter(Boolean);
    expect(hrefs).toContain("/dashboard");
    expect(hrefs).toContain("/scanner");
    expect(hrefs).toContain("/fraud-network");
    expect(hrefs).toContain("/scam-shield");
  });
});
