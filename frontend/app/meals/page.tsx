"use client";

import { useState, useRef } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Camera, Image as ImageIcon, Loader2, ArrowLeft, CheckCircle2 } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

// Test user UUID from backend config
const TEST_USER_ID = "550e8400-e29b-41d4-a716-446655440000";

interface VisionResponse {
    food_name: string;
    amount_g: number;
    calories: number;
    carbs_g: number;
    protein_g: number;
    fat_g: number;
    confidence: number;
    description: string;
}

export default function VisionLogPage() {
    const [image, setImage] = useState<string | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState<VisionResponse | null>(null);
    const [error, setError] = useState<string>("");
    const [isSaving, setIsSaving] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const router = useRouter();

    const handleImageCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        if (file.size > 5 * 1024 * 1024) {
            setError("Image size should be less than 5MB");
            return;
        }

        const reader = new FileReader();
        reader.onload = (event) => {
            setImage(event.target?.result as string);
            setResult(null);
            setError("");
        };
        reader.readAsDataURL(file);
    };

    const analyzeImage = async () => {
        if (!image) return;

        setIsAnalyzing(true);
        setError("");

        try {
            // For local testing, ensure backend is running at localhost:8000
            const response = await fetch("http://localhost:8000/api/meals/analyze-image", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    image_base64: image,
                    mime_type: "image/jpeg"
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to analyze image");
            }

            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "An error occurred");
        } finally {
            setIsAnalyzing(false);
        }
    };

    const saveMeal = async () => {
        if (!result) return;
        setIsSaving(true);
        setError("");

        try {
            const now = new Date();
            const hour = now.getHours();
            let meal_type = "snack";
            if (hour >= 5 && hour < 11) meal_type = "breakfast";
            else if (hour >= 11 && hour < 16) meal_type = "lunch";
            else if (hour >= 16 && hour < 22) meal_type = "dinner";

            const payload = {
                user_id: TEST_USER_ID,
                meal_type: meal_type,
                food_name: result.food_name,
                amount_g: result.amount_g,
                calories: result.calories,
                carbs_g: result.carbs_g,
                protein_g: result.protein_g,
                fat_g: result.fat_g,
                consumed_at: now.toISOString(),
            };

            const response = await fetch("http://localhost:8000/api/meals/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to save meal");
            }

            router.push("/");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to save meal. Is backend running?");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950 p-4 md:p-8">
            <div className="max-w-3xl mx-auto space-y-6">

                {/* Navigation */}
                <Link href="/" className="inline-flex items-center text-sm font-medium text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-50">
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back to Dashboard
                </Link>

                <div className="space-y-1">
                    <h1 className="text-3xl font-bold tracking-tight">Food Vision AI</h1>
                    <p className="text-neutral-500">Snap a photo of your meal and let AI do the counting.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                    {/* Image Upload Card */}
                    <Card className="flex flex-col border-neutral-200/60 dark:border-neutral-800 shadow-sm">
                        <CardHeader>
                            <CardTitle>1. Upload Photo</CardTitle>
                            <CardDescription>Take a picture or upload from gallery.</CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1 flex flex-col items-center justify-center min-h-[300px]">
                            {image ? (
                                <div className="relative w-full h-full rounded-lg overflow-hidden border border-neutral-200 dark:border-neutral-800">
                                    <img src={image} alt="Meal preview" className="w-full h-full object-cover" />
                                    <Button
                                        variant="secondary"
                                        size="sm"
                                        className="absolute top-2 right-2 bg-white/80 backdrop-blur-sm"
                                        onClick={() => setImage(null)}
                                    >
                                        Clear
                                    </Button>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center justify-center p-8 border-2 border-dashed border-neutral-200 dark:border-neutral-800 rounded-lg w-full h-full bg-neutral-50 dark:bg-neutral-900/50">
                                    <Camera className="w-12 h-12 text-neutral-400 mb-4" />
                                    <p className="text-sm text-neutral-500 text-center mb-4">
                                        Take a clear photo of your meal
                                    </p>
                                    <Input
                                        type="file"
                                        accept="image/*"
                                        className="hidden"
                                        ref={fileInputRef}
                                        onChange={handleImageCapture}
                                        capture="environment"
                                    />
                                    <div className="flex gap-3">
                                        <Button onClick={() => fileInputRef.current?.click()}>
                                            <Camera className="mr-2 w-4 h-4" /> Camera
                                        </Button>
                                        <Button variant="outline" onClick={() => {
                                            if (fileInputRef.current) {
                                                fileInputRef.current.removeAttribute('capture');
                                                fileInputRef.current.click();
                                            }
                                        }}>
                                            <ImageIcon className="mr-2 w-4 h-4" /> Gallery
                                        </Button>
                                    </div>
                                </div>
                            )}
                        </CardContent>
                        <CardFooter>
                            <Button
                                className="w-full bg-blue-600 hover:bg-blue-700"
                                disabled={!image || isAnalyzing}
                                onClick={analyzeImage}
                            >
                                {isAnalyzing ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Analyzing with Gemini 3.1...
                                    </>
                                ) : (
                                    "Analyze Meal"
                                )}
                            </Button>
                        </CardFooter>
                    </Card>

                    {/* Results Card */}
                    <Card className="flex flex-col shadow-sm border-neutral-200/60 dark:border-neutral-800">
                        <CardHeader>
                            <CardTitle>2. Verify & Save</CardTitle>
                            <CardDescription>Review the AI-extracted information.</CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1 space-y-4">

                            {error && (
                                <div className="p-3 bg-red-50 text-red-600 dark:bg-red-950/50 dark:text-red-400 rounded-md text-sm">
                                    {error}
                                </div>
                            )}

                            {!result && !error && (
                                <div className="flex flex-col items-center justify-center h-full text-center p-6 bg-neutral-50 dark:bg-neutral-900/50 rounded-lg">
                                    <p className="text-neutral-400 text-sm">Awaiting image analysis...</p>
                                </div>
                            )}

                            {result && (
                                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2">
                                    <div className="bg-blue-50 dark:bg-blue-950/30 p-4 rounded-lg border border-blue-100 dark:border-blue-900/30">
                                        <div className="flex justify-between items-start mb-2">
                                            <h3 className="font-semibold text-lg text-blue-900 dark:text-blue-100">{result.food_name}</h3>
                                            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                                                {(result.confidence * 100).toFixed(0)}% Match
                                            </span>
                                        </div>
                                        <p className="text-sm text-blue-700 dark:text-blue-300 mb-4">{result.description}</p>
                                        <p className="text-2xl font-bold tracking-tight text-blue-950 dark:text-blue-50">
                                            {result.calories} <span className="text-sm font-normal text-blue-700 dark:text-blue-300">kcal / {result.amount_g}g</span>
                                        </p>
                                    </div>

                                    <div className="space-y-4">
                                        <Label className="text-sm font-medium">Macros Details</Label>
                                        <div className="grid grid-cols-3 gap-3">
                                            <div className="p-3 bg-neutral-50 dark:bg-neutral-900/50 rounded-lg border border-neutral-200 dark:border-neutral-800 text-center">
                                                <span className="block text-xs text-neutral-500 mb-1">Carbs</span>
                                                <span className="font-semibold text-blue-600 dark:text-blue-400">{result.carbs_g}g</span>
                                            </div>
                                            <div className="p-3 bg-neutral-50 dark:bg-neutral-900/50 rounded-lg border border-neutral-200 dark:border-neutral-800 text-center">
                                                <span className="block text-xs text-neutral-500 mb-1">Protein</span>
                                                <span className="font-semibold text-emerald-600 dark:text-emerald-400">{result.protein_g}g</span>
                                            </div>
                                            <div className="p-3 bg-neutral-50 dark:bg-neutral-900/50 rounded-lg border border-neutral-200 dark:border-neutral-800 text-center">
                                                <span className="block text-xs text-neutral-500 mb-1">Fat</span>
                                                <span className="font-semibold text-amber-600 dark:text-amber-400">{result.fat_g}g</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                        </CardContent>
                        <CardFooter>
                            <Button
                                className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50"
                                disabled={!result || isSaving}
                                onClick={saveMeal}
                            >
                                {isSaving ? (
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                ) : (
                                    <CheckCircle2 className="mr-2 h-4 w-4" />
                                )}
                                {isSaving ? "Logging Meal..." : "Confirm & Log Meal"}
                            </Button>
                        </CardFooter>
                    </Card>

                </div>
            </div>
        </div>
    );
}
