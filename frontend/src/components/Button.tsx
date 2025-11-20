import { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {}

export function Button({ className = "", ...props }: ButtonProps) {
  return (
    <button
      className={`bg-foreground text-background py-2 px-4 rounded hover:bg-foreground/80 transition-colors disabled:opacity-50 ${className}`}
      {...props}
    />
  );
}