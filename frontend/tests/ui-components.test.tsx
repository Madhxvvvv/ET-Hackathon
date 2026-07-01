import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Alert } from "@/components/ui/Alert";
import { Spinner } from "@/components/ui/Spinner";
import { Skeleton } from "@/components/ui/Skeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { SearchBar } from "@/components/ui/SearchBar";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";

/* ─── Button ─── */
describe("Button", () => {
  it("renders children", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });

  it("shows loading spinner when loading=true and disables", () => {
    render(<Button loading>Save</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
  });

  it("calls onClick when not disabled", () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByRole("button"));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("does not call onClick when disabled", () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick} disabled>No click</Button>);
    fireEvent.click(screen.getByRole("button"));
    expect(onClick).not.toHaveBeenCalled();
  });
});

/* ─── Badge ─── */
describe("Badge", () => {
  it("renders text content", () => {
    render(<Badge>Active</Badge>);
    expect(screen.getByText("Active")).toBeInTheDocument();
  });
});

/* ─── Alert ─── */
describe("Alert", () => {
  it("renders with alert role", () => {
    render(<Alert>Watch out</Alert>);
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("renders title when provided", () => {
    render(<Alert title="Heads up">Content</Alert>);
    expect(screen.getByText("Heads up")).toBeInTheDocument();
  });
});

/* ─── Spinner ─── */
describe("Spinner", () => {
  it("has status role and default label", () => {
    render(<Spinner />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("accepts custom label", () => {
    render(<Spinner label="Processing" />);
    expect(screen.getByText("Processing")).toBeInTheDocument();
  });
});

/* ─── Skeleton ─── */
describe("Skeleton", () => {
  it("renders a placeholder div", () => {
    const { container } = render(<Skeleton className="h-8 w-32" />);
    expect(container.firstChild).toHaveClass("animate-pulse");
  });

  it("is hidden from assistive technology", () => {
    const { container } = render(<Skeleton />);
    expect(container.firstChild).toHaveAttribute("aria-hidden", "true");
  });
});

/* ─── EmptyState ─── */
describe("EmptyState", () => {
  it("renders title", () => {
    render(<EmptyState title="Nothing here" />);
    expect(screen.getByText("Nothing here")).toBeInTheDocument();
  });

  it("renders description", () => {
    render(<EmptyState title="Empty" description="Add some data to get started." />);
    expect(screen.getByText("Add some data to get started.")).toBeInTheDocument();
  });

  it("renders action button and calls onClick", () => {
    const onClick = jest.fn();
    render(<EmptyState title="Empty" action={{ label: "Add Item", onClick }} />);
    fireEvent.click(screen.getByRole("button", { name: "Add Item" }));
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});

/* ─── ErrorState ─── */
describe("ErrorState", () => {
  it("renders default title", () => {
    render(<ErrorState />);
    expect(screen.getByText("Something went wrong")).toBeInTheDocument();
  });

  it("renders retry button and calls onRetry", () => {
    const onRetry = jest.fn();
    render(<ErrorState onRetry={onRetry} />);
    fireEvent.click(screen.getByRole("button", { name: /try again/i }));
    expect(onRetry).toHaveBeenCalledTimes(1);
  });
});

/* ─── SearchBar ─── */
describe("SearchBar", () => {
  it("renders an input with searchbox role", () => {
    render(<SearchBar />);
    expect(screen.getByRole("searchbox")).toBeInTheDocument();
  });

  it("calls onSearch with typed value", () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);
    fireEvent.change(screen.getByRole("searchbox"), { target: { value: "fraud" } });
    expect(onSearch).toHaveBeenCalledWith("fraud");
  });

  it("shows clear button when value is present", () => {
    render(<SearchBar defaultValue="test" />);
    expect(screen.getByRole("button", { name: /clear/i })).toBeInTheDocument();
  });
});

/* ─── Card ─── */
describe("Card", () => {
  it("renders children", () => {
    render(
      <Card>
        <CardHeader><CardTitle>Test Card</CardTitle></CardHeader>
        <CardContent>Body</CardContent>
      </Card>
    );
    expect(screen.getByText("Test Card")).toBeInTheDocument();
    expect(screen.getByText("Body")).toBeInTheDocument();
  });
});
