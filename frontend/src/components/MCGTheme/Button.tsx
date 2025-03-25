import React from "react"

interface ButtonProps {
  href: string;
  title: string;
  children: React.ReactNode;
}

const Button = ({ href, title, children }: ButtonProps) => {
  return (
    <a href={href} title={title} class="">
      {children}
    </a>
  )
}

export default Button