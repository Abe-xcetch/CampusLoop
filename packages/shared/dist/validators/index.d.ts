import { z } from "zod";
/**
 * User Auth & Signup Validators
 */
export declare const SignUpSchema: z.ZodObject<{
    email: z.ZodString;
    firstName: z.ZodString;
    lastName: z.ZodString;
    password: z.ZodString;
    phoneNumber: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    email: string;
    firstName: string;
    lastName: string;
    password: string;
    phoneNumber?: string | undefined;
}, {
    email: string;
    firstName: string;
    lastName: string;
    password: string;
    phoneNumber?: string | undefined;
}>;
export declare const LoginSchema: z.ZodObject<{
    email: z.ZodString;
    password: z.ZodString;
}, "strip", z.ZodTypeAny, {
    email: string;
    password: string;
}, {
    email: string;
    password: string;
}>;
/**
 * Marketplace Listing Validators
 */
export declare const CreateListingSchema: z.ZodObject<{
    title: z.ZodString;
    description: z.ZodString;
    price: z.ZodNumber;
    condition: z.ZodEnum<["NEW", "LIKE_NEW", "GOOD", "FAIR"]>;
    categoryId: z.ZodString;
    mediaUrls: z.ZodArray<z.ZodString, "many">;
}, "strip", z.ZodTypeAny, {
    title: string;
    description: string;
    price: number;
    condition: "NEW" | "LIKE_NEW" | "GOOD" | "FAIR";
    categoryId: string;
    mediaUrls: string[];
}, {
    title: string;
    description: string;
    price: number;
    condition: "NEW" | "LIKE_NEW" | "GOOD" | "FAIR";
    categoryId: string;
    mediaUrls: string[];
}>;
/**
 * Transaction Review Validators
 */
export declare const CreateReviewSchema: z.ZodObject<{
    transactionId: z.ZodString;
    rating: z.ZodNumber;
    comment: z.ZodString;
}, "strip", z.ZodTypeAny, {
    transactionId: string;
    rating: number;
    comment: string;
}, {
    transactionId: string;
    rating: number;
    comment: string;
}>;
/**
 * Fraud Moderation Report Validators
 */
export declare const CreateReportSchema: z.ZodEffects<z.ZodObject<{
    reportedUserId: z.ZodOptional<z.ZodString>;
    reportedListingId: z.ZodOptional<z.ZodString>;
    reason: z.ZodNativeEnum<{
        readonly FRAUD_SCAM: "FRAUD_SCAM";
        readonly INAPPROPRIATE_CONTENT: "INAPPROPRIATE_CONTENT";
        readonly COUNTERFEIT: "COUNTERFEIT";
        readonly OUT_OF_STOCK_SPAM: "OUT_OF_STOCK_SPAM";
        readonly OTHER: "OTHER";
    }>;
    details: z.ZodString;
}, "strip", z.ZodTypeAny, {
    reason: "FRAUD_SCAM" | "INAPPROPRIATE_CONTENT" | "COUNTERFEIT" | "OUT_OF_STOCK_SPAM" | "OTHER";
    details: string;
    reportedUserId?: string | undefined;
    reportedListingId?: string | undefined;
}, {
    reason: "FRAUD_SCAM" | "INAPPROPRIATE_CONTENT" | "COUNTERFEIT" | "OUT_OF_STOCK_SPAM" | "OTHER";
    details: string;
    reportedUserId?: string | undefined;
    reportedListingId?: string | undefined;
}>, {
    reason: "FRAUD_SCAM" | "INAPPROPRIATE_CONTENT" | "COUNTERFEIT" | "OUT_OF_STOCK_SPAM" | "OTHER";
    details: string;
    reportedUserId?: string | undefined;
    reportedListingId?: string | undefined;
}, {
    reason: "FRAUD_SCAM" | "INAPPROPRIATE_CONTENT" | "COUNTERFEIT" | "OUT_OF_STOCK_SPAM" | "OTHER";
    details: string;
    reportedUserId?: string | undefined;
    reportedListingId?: string | undefined;
}>;
//# sourceMappingURL=index.d.ts.map