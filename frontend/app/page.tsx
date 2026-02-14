export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">
          Nutri-Agent Flow
        </h1>
        <p className="text-center text-muted-foreground mb-4">
          AI-powered nutrition management and meal recommendation system
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
          <div className="p-6 border rounded-lg hover:border-primary transition-colors">
            <h2 className="text-xl font-semibold mb-2">Meal Logging</h2>
            <p className="text-sm text-muted-foreground">
              Record your meals and automatically calculate nutritional values
            </p>
          </div>
          <div className="p-6 border rounded-lg hover:border-primary transition-colors">
            <h2 className="text-xl font-semibold mb-2">Nutrient Rebalancing</h2>
            <p className="text-sm text-muted-foreground">
              Real-time analysis of your remaining daily nutrients
            </p>
          </div>
          <div className="p-6 border rounded-lg hover:border-primary transition-colors">
            <h2 className="text-xl font-semibold mb-2">Recipe Recommendations</h2>
            <p className="text-sm text-muted-foreground">
              AI-powered recipe suggestions based on your nutrition needs
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
