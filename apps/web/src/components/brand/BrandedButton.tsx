"use client";
import React from "react";
import { Button, ButtonProps } from "../ui/Button";

export function BrandedButton(props: Omit<ButtonProps, 'variant'> & { variant?: ButtonProps['variant'] }) {
  return <Button variant={props.variant || 'primary'} {...props} />;
}
