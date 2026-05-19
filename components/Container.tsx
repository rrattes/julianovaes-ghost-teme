import type { ReactNode } from "react";

type ContainerProps = {
  children: ReactNode;
  className?: string;
};

export function Container({ children, className = "" }: ContainerProps) {
  return <div className={`mx-auto w-[min(1180px,calc(100%_-_32px))] ${className}`}>{children}</div>;
}
