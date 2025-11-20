import { InputHTMLAttributes } from "react";

interface AmountInputProps extends InputHTMLAttributes<HTMLInputElement> {}

export function AmountInput({ className = "", ...props }: AmountInputProps) {
  return (
    <input
      type="number"
      step="0.0001"
      min="0"
      className={`w-full p-2 border border-foreground/20 rounded focus:outline-none focus:ring-2 focus:ring-foreground/50 ${className}`}
      {...props}
    />
  );
}