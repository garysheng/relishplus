"""
Configuration for RelishPlus automation
"""
from dataclasses import dataclass
from typing import List, Optional
import os
import yaml
from dotenv import load_dotenv

@dataclass
class DietaryPreferences:
    """Dietary preferences configuration"""
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_halal: bool = False
    is_kosher: bool = False
    avoid_ingredients: List[str] = None

@dataclass
class Config:
    """Main configuration class"""
    dietary_preferences: DietaryPreferences
    preferred_cuisines: Optional[List[str]] = None
    delivery_instructions: Optional[str] = None

def load_config() -> Config:
    """Load configuration from environment and config file"""
    load_dotenv()
    
    # Load from config.yml if it exists
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
    else:
        config_data = {}
        
    # Extract dietary preferences
    dietary_prefs = config_data.get("dietary_preferences", {})
    dietary_preferences = DietaryPreferences(
        is_vegetarian=dietary_prefs.get("is_vegetarian", False),
        is_vegan=dietary_prefs.get("is_vegan", False),
        is_gluten_free=dietary_prefs.get("is_gluten_free", False),
        is_halal=dietary_prefs.get("is_halal", False),
        is_kosher=dietary_prefs.get("is_kosher", False),
        avoid_ingredients=dietary_prefs.get("avoid_ingredients", [])
    )
    
    # Create config object
    return Config(
        dietary_preferences=dietary_preferences,
        preferred_cuisines=config_data.get("preferred_cuisines"),
        delivery_instructions=config_data.get("delivery_instructions")
    ) 