# RelishPlus Data Model

## Configuration

The system uses a JSON-based configuration system to store user preferences and automation settings.

### HealthPreference

```typescript
enum HealthPreference {
  VERY_HEALTHY = "very_healthy",     // Salads, grain bowls, lean proteins
  MODERATELY_HEALTHY = "moderately_healthy", // Balance of healthy and comfort food
  NO_PREFERENCE = "no_preference"     // Any type of food
}
```

### DietaryPreferences

```typescript
interface DietaryPreferences {
  isVegetarian: boolean;
  isVegan: boolean;
  isGlutenFree: boolean;
  isDairyFree: boolean;
  isHalal: boolean;
  isKosher: boolean;
  avoidIngredients: string[];  // Specific ingredients to avoid
}
```

### Config

Main configuration structure:

```typescript
interface Config {
  healthPreference: HealthPreference;
  dietaryPreferences: DietaryPreferences;
  preferredCuisines: string[];
  deliveryInstructions?: string;
}
```

## Workflow Data Model

### Restaurant

```typescript
interface Restaurant {
  name: string;
  description: string;
  cuisine: string;
  healthScore: number;  // 1-10 scale
  orderByTime: string;  // Format: "HH:MM AM/PM"
  deliveryTime: string; // Format: "HH:MM AM/PM"
  dietaryOptions: {
    hasVegetarian: boolean;
    hasVegan: boolean;
    hasGlutenFree: boolean;
    hasDairyFree: boolean;
    hasHalal: boolean;
    hasKosher: boolean;
  };
}
```

### MenuItem

```typescript
interface MenuItem {
  name: string;
  price: number;  // Must be under $20 after tax
  description: string;
  healthScore: number;  // 1-10 scale
  ingredients: string[];
  dietaryInfo: {
    isVegetarian: boolean;
    isVegan: boolean;
    isGlutenFree: boolean;
    isDairyFree: boolean;
    isHalal: boolean;
    isKosher: boolean;
  };
  options?: {
    name: string;
    choices: string[];
    price?: number;
  }[];
}
```

### Order

```typescript
interface Order {
  restaurant: string;
  items: {
    name: string;
    options?: string[];
    price: number;
  }[];
  deliveryInstructions?: string;
  subtotal: number;
  deliveryFee: number;
  tax: number;
  companySubsidy: number;
  total: number;  // Must be $0 after subsidy
}
```

## File Structure

```
relishplus/
├── config.json           # User configuration
├── .env                 # Environment variables
└── logs/               # Automation logs
```

## Environment Variables

- `RELISH_EMAIL`: Login email for Relish account
- `RELISH_PASSWORD`: Login password for Relish account
- `OPENAI_API_KEY`: OpenAI API key for potential future AI features 