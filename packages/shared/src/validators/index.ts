import { z } from "zod";
import { STRATHMORE_EMAIL_REGEX, REPORT_REASONS } from "../constants/index.js";

/**
 * User Auth & Signup Validators
 */
export const SignUpSchema = z.object({
  email: z
    .string()
    .email("Invalid email address")
    .regex(
      STRATHMORE_EMAIL_REGEX,
      "Only Strathmore University emails (@strathmore.edu or @su.strathmore.edu) are allowed"
    ),
  firstName: z.string().min(2, "First name must be at least 2 characters"),
  lastName: z.string().min(2, "Last name must be at least 2 characters"),
  password: z.string().min(8, "Password must be at least 8 characters long"),
  phoneNumber: z
    .string()
    .regex(/^\+254[17]\d{8}$/, "Phone number must be Kenyan format (+254...)")
    .optional()
});

export const LoginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required")
});

/**
 * Marketplace Listing Validators
 */
export const CreateListingSchema = z.object({
  title: z
    .string()
    .min(5, "Title must be at least 5 characters")
    .max(100, "Title is too long"),
  description: z
    .string()
    .min(20, "Description must be at least 20 characters")
    .max(1000, "Description is too long"),
  price: z.number().positive("Price must be greater than 0"),
  condition: z.enum(["NEW", "LIKE_NEW", "GOOD", "FAIR"]),
  categoryId: z.string().uuid("Invalid category ID"),
  mediaUrls: z
    .array(z.string().url("Invalid image URL"))
    .min(1, "At least one image is required")
    .max(5, "Maximum of 5 images allowed")
});

/**
 * Transaction Review Validators
 */
export const CreateReviewSchema = z.object({
  transactionId: z.string().uuid("Invalid transaction ID"),
  rating: z
    .number()
    .int()
    .min(1, "Rating must be at least 1 star")
    .max(5, "Rating cannot exceed 5 stars"),
  comment: z
    .string()
    .min(5, "Comment must be at least 5 characters")
    .max(500, "Comment is too long")
});

/**
 * Fraud Moderation Report Validators
 */
export const CreateReportSchema = z.object({
  reportedUserId: z.string().optional(),
  reportedListingId: z.string().optional(),
  reason: z.nativeEnum(REPORT_REASONS),
  details: z
    .string()
    .min(10, "Details must provide at least 10 characters explanation")
    .max(1000, "Report details are too long")
}).refine(
  (data) => data.reportedUserId || data.reportedListingId,
  {
    message: "A report must target either a listing or a user",
    path: ["reportedUserId"]
  }
);
