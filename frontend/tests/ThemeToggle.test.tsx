import { render, screen } from "@testing-library/react";

const mockSetTheme = jest.fn();
jest.mock("next-themes", () => ({
  useTheme: () => ({
    resolvedTheme: "light",
    setTheme: mockSetTheme,
    theme: "light",
  }),
  ThemeProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

// Simulate mounted=true so the real button renders instead of the disabled placeholder
jest.mock("react", () => {
  const actual = jest.requireActual<typeof import("react")>("react");
  return {
    ...actual,
    useState: (init: unknown) => {
      if (init === false) return [true, jest.fn()]; // override mounted state
      return actual.useState(init);
    },
  };
});

import { ThemeToggle } from "@/components/ui/ThemeToggle";

describe("ThemeToggle", () => {
  beforeEach(() => { mockSetTheme.mockClear(); });

  it("renders a button with accessible label", () => {
    render(<ThemeToggle />);
    const btn = screen.getByRole("button");
    expect(btn).toBeInTheDocument();
    expect(btn).toHaveAttribute("aria-label");
  });

  it("aria-label mentions mode switching", () => {
    render(<ThemeToggle />);
    const btn = screen.getByRole("button");
    expect(btn.getAttribute("aria-label")).toMatch(/switch to (dark|light) mode/i);
  });
});
