"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CreateReportSchema = exports.CreateReviewSchema = exports.CreateListingSchema = exports.LoginSchema = exports.SignUpSchema = void 0;
const zod_1 = require("zod");
const index_js_1 = require("../constants/index.js");
/**
 * User Auth & Signup Validators
 */
exports.SignUpSchema = zod_1.z.object({
    email: zod_1.z
        .string()
        .email("Invalid email address")
        .regex(index_js_1.STRATHMORE_EMAIL_REGEX, "Only Strathmore University emails (@strathmore.edu or @su.strathmore.edu) are allowed"),
    firstName: zod_1.z.string().min(2, "First name must be at least 2 characters"),
    lastName: zod_1.z.string().min(2, "Last name must be at least 2 characters"),
    password: zod_1.z.string().min(8, "Password must be at least 8 characters long"),
    phoneNumber: zod_1.z
        .string()
        .regex(/^\+254[17]\d{8}$/, "Phone number must be Kenyan format (+254...)")
        .optional()
});
exports.LoginSchema = zod_1.z.object({
    email: zod_1.z.string().email("Invalid email address"),
    password: zod_1.z.string().min(1, "Password is required")
});
/**
 * Marketplace Listing Validators
 */
exports.CreateListingSchema = zod_1.z.object({
    title: zod_1.z
        .string()
        .min(5, "Title must be at least 5 characters")
        .max(100, "Title is too long"),
    description: zod_1.z
        .string()
        .min(20, "Description must be at least 20 characters")
        .max(1000, "Description is too long"),
    price: zod_1.z.number().positive("Price must be greater than 0"),
    condition: zod_1.z.enum(["NEW", "LIKE_NEW", "GOOD", "FAIR"]),
    categoryId: zod_1.z.string().uuid("Invalid category ID"),
    mediaUrls: zod_1.z
        .array(zod_1.z.string().url("Invalid image URL"))
        .min(1, "At least one image is required")
        .max(5, "Maximum of 5 images allowed")
});
/**
 * Transaction Review Validators
 */
exports.CreateReviewSchema = zod_1.z.object({
    transactionId: zod_1.z.string().uuid("Invalid transaction ID"),
    rating: zod_1.z
        .number()
        .int()
        .min(1, "Rating must be at least 1 star")
        .max(5, "Rating cannot exceed 5 stars"),
    comment: zod_1.z
        .string()
        .min(5, "Comment must be at least 5 characters")
        .max(500, "Comment is too long")
});
/**
 * Fraud Moderation Report Validators
 */
exports.CreateReportSchema = zod_1.z.object({
    reportedUserId: zod_1.z.string().optional(),
    reportedListingId: zod_1.z.string().optional(),
    reason: zod_1.z.nativeEnum(index_js_1.REPORT_REASONS),
    details: zod_1.z
        .string()
        .min(10, "Details must provide at least 10 characters explanation")
        .max(1000, "Report details are too long")
}).refine((data) => data.reportedUserId || data.reportedListingId, {
    message: "A report must target either a listing or a user",
    path: ["reportedUserId"]
});
//# sourceMappingURL=index.js.map