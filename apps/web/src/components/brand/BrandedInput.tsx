"use client";
import React from "react";
import Input from "../ui/Input";

export default function BrandedInput(props: React.ComponentProps<typeof Input>) {
  return <Input {...props} />;
}
