import { InputHTMLAttributes } from "react";

interface AddressInputProps extends InputHTMLAttributes<HTMLInputElement> {}

export function AddressInput({ className = "", ...props }: AddressInputProps) {
  return (  
    <input
      type="text"
      className={`w-full p-2 border border-foreground/20 rounded focus:outline-none focus:ring-2 focus:ring-foreground/50 ${className}`}
      {...props}
    />
  );
}