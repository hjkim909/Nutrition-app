"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Camera, Plus, Activity, Droplets, Flame, Beef } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip } from "recharts";
import Link from "next/link";

// Test user UUID from backend config
const TEST_USER_ID = "550e8400-e29b-41d4-a716-446655440000";

interface NutritionData {
  calories: number;
  carbs: number;
  protein: number;
  fat: number;
}

interface Meal {
  id: string;
  name: string;
  time: string;
  call: number;
}

export default function DashboardPage() {
  const [mounted, setMounted] = useState(false);
  const [nutritionGoals] = useState<NutritionData>({ calories: 2200, carbs: 250, protein: 150, fat: 70 });
  const [todayConsumed, setTodayConsumed] = useState<NutritionData>({ calories: 0, carbs: 0, protein: 0, fat: 0 });
  const [mealHistory, setMealHistory] = useState<Meal[]>([]);
  const [aiAdvice, setAiAdvice] = useState<{ warnings: string[], recommendations: string } | null>(null);

  useEffect(() => {
    setMounted(true);
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];

      // Fetch balance
      const balanceRes = await fetch(`http://localhost:8000/api/meals/nutrition/balance?user_id=${TEST_USER_ID}&date=${today}`);
      if (balanceRes.ok) {
        const balanceData = await balanceRes.json();
        setTodayConsumed({
          calories: balanceData.consumed?.calories || 0,
          carbs: balanceData.consumed?.carbs_g || 0,
          protein: balanceData.consumed?.protein_g || 0,
          fat: balanceData.consumed?.fat_g || 0,
        });
        setAiAdvice({
          warnings: balanceData.warnings || [],
          recommendations: balanceData.recommendations || "Keep up the good work!"
        });
      }

      // Fetch meals
      const mealsRes = await fetch(`http://localhost:8000/api/meals/?user_id=${TEST_USER_ID}&date_from=${today}&date_to=${today}`);
      if (mealsRes.ok) {
        const mealsData = await mealsRes.json();
        const formattedMeals = mealsData.map((m: any) => ({
          id: m.id,
          name: m.food_name,
          time: new Date(m.consumed_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          call: m.calories
        }));
        // Ensure most recent meals are at the top
        setMealHistory(formattedMeals.reverse());
      }
    } catch (e) {
      console.error(e);
    }
  };

  if (!mounted) return null;

  const calProgress = (todayConsumed.calories / nutritionGoals.calories) * 100;

  const macroData = [
    { name: 'Carbs', value: todayConsumed.carbs, color: '#3b82f6' },
    { name: 'Protein', value: todayConsumed.protein, color: '#10b981' },
    { name: 'Fat', value: todayConsumed.fat, color: '#f59e0b' },
  ];

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-50 px-4 py-8 md:p-8">
      <div className="max-w-6xl mx-auto space-y-8">

        {/* Header Section */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight">Mechu Dashboard</h1>
            <p className="text-neutral-500 dark:text-neutral-400 mt-1">
              Your AI-powered nutrition strategist.
            </p>
          </div>
          <div className="flex gap-3">
            <Link href="/meals">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white shadow-lg transition-all" size="lg">
                <Camera className="mr-2 h-5 w-5" />
                Vision Log
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="shadow-sm">
              <Plus className="mr-2 h-5 w-5" />
              Manual Log
            </Button>
          </div>
        </header>

        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          {/* Main Calorie Card */}
          <Card className="md:col-span-2 shadow-sm border-neutral-200/60 dark:border-neutral-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-xl flex items-center gap-2">
                <Flame className="text-orange-500 w-5 h-5" />
                Today&apos;s Calories
              </CardTitle>
              <CardDescription>Daily energy budget overview</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col md:flex-row items-center justify-between gap-8 py-4">
                <div className="w-full md:w-1/2 space-y-2">
                  <div className="flex justify-between items-end">
                    <span className="text-5xl font-extrabold tracking-tighter">
                      {Math.round(todayConsumed.calories)}
                      <span className="text-lg text-neutral-400 font-medium ml-1">/ {nutritionGoals.calories} kcal</span>
                    </span>
                  </div>
                  <Progress value={calProgress} className="h-3 w-full bg-neutral-100 dark:bg-neutral-800" />
                  <p className="text-sm text-neutral-500 dark:text-neutral-400 pt-1 font-medium">
                    {Math.max(0, nutritionGoals.calories - Math.round(todayConsumed.calories))} kcal remaining
                  </p>
                </div>

                <div className="w-full md:w-1/2 h-[180px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={macroData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {macroData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <RechartsTooltip
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        itemStyle={{ color: '#111827', fontWeight: 500 }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* AI Strategy Insights Card */}
          <Card className="shadow-sm border-neutral-200/60 dark:border-neutral-800 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-blue-700 dark:text-blue-400">
                <Activity className="w-5 h-5" />
                Nutri-Strategist
              </CardTitle>
              <CardDescription className="text-blue-600/80 dark:text-blue-300/80">AI Analysis & Advice</CardDescription>
            </CardHeader>
            <CardContent>
              {aiAdvice ? (
                <div className="space-y-4">
                  {aiAdvice.warnings.map((warning, i) => (
                    <div key={i} className="flex items-start gap-3 bg-white/60 dark:bg-neutral-900/40 p-3 rounded-lg border border-blue-100 dark:border-blue-900/30">
                      <div className="text-sm">
                        <span className="font-semibold text-neutral-900 dark:text-neutral-100 block mb-1">Warning</span>
                        <span className="text-neutral-600 dark:text-neutral-400 leading-relaxed">{warning}</span>
                      </div>
                    </div>
                  ))}
                  <div className="flex items-start gap-3 bg-white/60 dark:bg-neutral-900/40 p-3 rounded-lg border border-blue-100 dark:border-blue-900/30">
                    <div className="text-sm">
                      <span className="font-semibold text-neutral-900 dark:text-neutral-100 block mb-1">Recommendation</span>
                      <span className="text-neutral-600 dark:text-neutral-400 leading-relaxed">{aiAdvice.recommendations}</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-neutral-500 text-center py-4">Awaiting analytics...</div>
              )}
            </CardContent>
          </Card>

          {/* Macros Breakdown */}
          <Card className="md:col-span-2 shadow-sm border-neutral-200/60 dark:border-neutral-800">
            <CardHeader>
              <CardTitle className="text-lg">Macronutrients Progress</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="flex items-center gap-1.5 font-medium">
                    <div className="w-3 h-3 rounded-full bg-blue-500"></div> Carbs
                  </span>
                  <span className="text-neutral-500 font-medium">{Math.round(todayConsumed.carbs)}g / {nutritionGoals.carbs}g</span>
                </div>
                <Progress value={(todayConsumed.carbs / nutritionGoals.carbs) * 100} className="h-2" style={{ "--progress-background": "#3b82f6" } as React.CSSProperties} indicatorColor="bg-blue-500" />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="flex items-center gap-1.5 font-medium">
                    <div className="w-3 h-3 rounded-full bg-emerald-500"></div> Protein
                  </span>
                  <span className="text-neutral-500 font-medium">{Math.round(todayConsumed.protein)}g / {nutritionGoals.protein}g</span>
                </div>
                <Progress value={(todayConsumed.protein / nutritionGoals.protein) * 100} className="h-2" indicatorColor="bg-emerald-500" />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="flex items-center gap-1.5 font-medium">
                    <div className="w-3 h-3 rounded-full bg-amber-500"></div> Fat
                  </span>
                  <span className="text-neutral-500 font-medium">{Math.round(todayConsumed.fat)}g / {nutritionGoals.fat}g</span>
                </div>
                <Progress value={(todayConsumed.fat / nutritionGoals.fat) * 100} className="h-2" indicatorColor="bg-amber-500" />
              </div>
            </CardContent>
          </Card>

          {/* Today's Meals List */}
          <Card className="shadow-sm border-neutral-200/60 dark:border-neutral-800 flex flex-col">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg flex justify-between items-center">
                Today&apos;s Log
                <span className="text-xs font-normal text-neutral-500 bg-neutral-100 dark:bg-neutral-800 px-2 py-1 rounded-full">{mealHistory.length} items</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 p-0">
              <ScrollArea className="h-[250px] w-full border-t border-neutral-100 dark:border-neutral-800">
                <div className="p-4 space-y-4">
                  {mealHistory.length === 0 && (
                    <p className="text-sm text-neutral-500 text-center py-8">No meals logged today yet.</p>
                  )}
                  {mealHistory.map((meal) => (
                    <div key={meal.id} className="flex justify-between items-center group">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center group-hover:bg-blue-50 dark:group-hover:bg-blue-900/30 transition-colors">
                          <Beef className="w-5 h-5 text-neutral-500 group-hover:text-blue-500 transition-colors" />
                        </div>
                        <div>
                          <p className="text-sm font-semibold truncate max-w-[150px]">{meal.name}</p>
                          <p className="text-xs text-neutral-500">{meal.time}</p>
                        </div>
                      </div>
                      <span className="text-sm font-medium whitespace-nowrap">{meal.call} kcal</span>
                    </div>
                  ))}
                </div>
              </ScrollArea>
              <div className="p-4 border-t border-neutral-100 dark:border-neutral-800 bg-neutral-50/50 dark:bg-neutral-900/50">
                <Button variant="ghost" className="w-full text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300">View Full History</Button>
              </div>
            </CardContent>
          </Card>

        </div>
      </div>
    </div>
  );
}
