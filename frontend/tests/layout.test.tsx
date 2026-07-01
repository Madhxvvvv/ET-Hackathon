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

import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Footer } from "@/components/layout/Footer";
import { PageHeader } from "@/components/layout/PageHeader";

describe("DashboardLayout", () => {
  it("renders children inside main content area", () => {
    render(
      <DashboardLayout>
        <div data-testid="content">Page content</div>
      </DashboardLayout>
    );
    expect(screen.getByTestId("content")).toBeInTheDocument();
  });

  it("renders sidebar navigation", () => {
    render(<DashboardLayout><div /></DashboardLayout>);
    expect(screen.getByRole("complementary", { name: /main navigation/i })).toBeInTheDocument();
  });

  it("renders footer", () => {
    render(<DashboardLayout><div /></DashboardLayout>);
    expect(screen.getByRole("contentinfo")).toBeInTheDocument();
  });

  it("main content area has correct id", () => {
    render(<DashboardLayout><div /></DashboardLayout>);
    expect(document.getElementById("main-content")).toBeInTheDocument();
  });
});

describe("Footer", () => {
  it("renders contentinfo landmark", () => {
    render(<Footer />);
    expect(screen.getByRole("contentinfo")).toBeInTheDocument();
  });

  it("contains platform name", () => {
    render(<Footer />);
    expect(screen.getByText(/digital public safety platform/i)).toBeInTheDocument();
  });
});

describe("PageHeader", () => {
  it("renders title as h1", () => {
    render(<PageHeader title="Test Page" />);
    expect(screen.getByRole("heading", { level: 1, name: "Test Page" })).toBeInTheDocument();
  });

  it("renders description", () => {
    render(<PageHeader title="Test" description="Some description" />);
    expect(screen.getByText("Some description")).toBeInTheDocument();
  });

  it("renders actions slot", () => {
    render(<PageHeader title="Test" actions={<button>Action</button>} />);
    expect(screen.getByRole("button", { name: "Action" })).toBeInTheDocument();
  });
});
