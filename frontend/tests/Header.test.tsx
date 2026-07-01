import { render, screen } from "@testing-library/react";

jest.mock("next-themes", () => ({
  useTheme: () => ({ resolvedTheme: "light", setTheme: jest.fn() }),
  ThemeProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

jest.mock("next/navigation", () => ({
  usePathname: () => "/dashboard",
}));

jest.mock("next/link", () => {
  return function MockLink({ children, href }: { children: React.ReactNode; href: string }) {
    return <a href={href}>{children}</a>;
  };
});

import { TopNav } from "@/components/layout/TopNav";

describe("Header (TopNav)", () => {
  it("has accessible banner role", () => {
    render(<TopNav onSidebarToggle={jest.fn()} isSidebarOpen={false} />);
    expect(screen.getByRole("banner")).toBeInTheDocument();
  });

  it("contains a search input", () => {
    render(<TopNav onSidebarToggle={jest.fn()} isSidebarOpen={false} />);
    expect(screen.getByRole("searchbox")).toBeInTheDocument();
  });

  it("displays user avatar", () => {
    render(<TopNav onSidebarToggle={jest.fn()} isSidebarOpen={false} />);
    expect(screen.getByTitle(/analyst account/i)).toBeInTheDocument();
  });
});
