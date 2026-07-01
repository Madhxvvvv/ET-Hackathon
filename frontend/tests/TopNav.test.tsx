import { render, screen, fireEvent } from "@testing-library/react";

jest.mock("next-themes", () => ({
  useTheme: () => ({ resolvedTheme: "light", setTheme: jest.fn(), theme: "light" }),
  ThemeProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

import { TopNav } from "@/components/layout/TopNav";

describe("TopNav", () => {
  it("renders header landmark", () => {
    render(<TopNav onSidebarToggle={jest.fn()} isSidebarOpen={false} />);
    expect(screen.getByRole("banner")).toBeInTheDocument();
  });

  it("renders search bar", () => {
    render(<TopNav onSidebarToggle={jest.fn()} isSidebarOpen={false} />);
    expect(screen.getByRole("searchbox")).toBeInTheDocument();
  });

  it("calls onSidebarToggle when menu button is clicked", () => {
    const toggle = jest.fn();
    render(<TopNav onSidebarToggle={toggle} isSidebarOpen={false} />);
    const menuButtons = screen.getAllByRole("button", { name: /sidebar/i });
    fireEvent.click(menuButtons[0]);
    expect(toggle).toHaveBeenCalledTimes(1);
  });

  it("renders notification bell", () => {
    render(<TopNav onSidebarToggle={jest.fn()} isSidebarOpen={false} />);
    expect(screen.getByRole("button", { name: /notifications/i })).toBeInTheDocument();
  });

  it("renders theme toggle button", () => {
    render(<TopNav onSidebarToggle={jest.fn()} isSidebarOpen={false} />);
    // Theme toggle has aria-label "Switch to dark mode" or "Switch to light mode"
    const themeBtn = screen.getByRole("button", { name: /switch to (dark|light) mode/i });
    expect(themeBtn).toBeInTheDocument();
  });
});
