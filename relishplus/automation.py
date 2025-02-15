"""
Browser automation for Relish/ezCater ordering system
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
from browser_use import Agent
from langchain_openai import ChatOpenAI
from .config import Config
import asyncio

logger = logging.getLogger(__name__)

class RelishAutomation:
    """Handles browser automation for Relish ordering"""
    
    def __init__(self, email: str, password: str, config: Config):
        self.email = email
        self.password = password
        self.config = config
        self.llm = ChatOpenAI(model="gpt-4o")
        self.login_url = "https://login.ezcater.com/relish/sessions/new"
        self.base_url = "https://relish.ezcater.com"
        self.max_pretax_price = 18.00  # $19.49 after tax
        self.agent = None

    def _get_dietary_restrictions_text(self) -> str:
        """Generate text description of dietary restrictions"""
        restrictions = []
        if self.config.dietary_preferences.is_vegetarian:
            restrictions.append("- Must be vegetarian")
        if self.config.dietary_preferences.is_vegan:
            restrictions.append("- Must be vegan")
        if self.config.dietary_preferences.is_gluten_free:
            restrictions.append("- Must be gluten-free")
        if self.config.dietary_preferences.is_halal:
            restrictions.append("- Must be halal")
        if self.config.dietary_preferences.is_kosher:
            restrictions.append("- Must be kosher")
        if self.config.dietary_preferences.avoid_ingredients:
            restrictions.append(f"- Must avoid these ingredients: {', '.join(self.config.dietary_preferences.avoid_ingredients)}")
        
        if not restrictions:
            return "No specific dietary restrictions."
        return "Dietary Restrictions:\n" + "\n".join(restrictions)

    async def order_all_days(self) -> bool:
        """Process orders for all days through Saturday"""
        try:
            # Get current date and next 5 days
            today = datetime.now()
            dates = [(today + timedelta(days=i)) for i in range(6)]
            dates_str = "\n      ".join([d.strftime("%A %m/%d") for d in dates])
            date_urls = {d.strftime("%A %m/%d"): f"{self.base_url}/schedule/{d.strftime('%Y-%m-%d')}" for d in dates}

            dietary_restrictions = self._get_dietary_restrictions_text()

            task = (
                f"Complete the following sequence of actions:\n\n"
                f"1. Go to {self.login_url}\n"
                f"2. Log in with email '{self.email}' and password '{self.password}'\n"
                f"3. If you see a welcome screen with 'Let\'s Go!' button, click it\n"
                f"4. Process these 6 dates in order (today through next 5 days):\n"
                f"      {dates_str}\n\n"
                f"5. For each date, complete BOTH lunch and dinner before moving to next date:\n"
                f"   a. Navigate directly to the date's URL (e.g. {self.base_url}/schedule/YYYY-MM-DD)\n"
                f"   b. Look for the LUNCH header and check if lunch is already ordered (look for 'Preparing Your Order', 'Order Placed', etc)\n"
                f"   c. If lunch isn't ordered:\n"
                f"      - Find restaurants with healthy options (salads, grain bowls, lean proteins) that match dietary restrictions\n"
                f"      - Look for and scroll to any section containing main dishes first (like 'Entrées', 'Main Courses', 'Bowls', 'Plates', etc)\n"
                f"      - First add a healthy main dish to cart (prioritize protein-rich meals)\n"
                f"      - Before adding any item, check that it won't exceed ${self.max_pretax_price} pretax total\n"
                f"      - Add healthy sides/extras until reaching AT LEAST $15.00 of the subsidy\n"
                f"      - Continue adding items until close to but NOT EXCEEDING ${self.max_pretax_price}\n"
                f"      - If an item's 'Add to Cart' button is not visible/clickable, try a different item\n"
                f"      - NEVER checkout with less than $15.00 of items unless absolutely no other options exist\n"
                f"      - ALWAYS click 'Proceed to Checkout' and complete the order\n"
                f"      - After checkout, ALWAYS return to the specific date's URL to continue with dinner\n"
                f"   d. Look for the DINNER header and check if dinner is already ordered\n"
                f"   e. If dinner isn't ordered:\n"
                f"      - Find restaurants with healthy options (salads, grain bowls, lean proteins) that match dietary restrictions\n"
                f"      - Look for and scroll to any section containing main dishes first (like 'Entrées', 'Main Courses', 'Bowls', 'Plates', etc)\n"
                f"      - First add a healthy main dish to cart (prioritize protein-rich meals)\n"
                f"      - Before adding any item, check that it won't exceed ${self.max_pretax_price} pretax total\n"
                f"      - Add healthy sides/extras until reaching AT LEAST $15.00 of the subsidy\n"
                f"      - Continue adding items until close to but NOT EXCEEDING ${self.max_pretax_price}\n"
                f"      - If an item's 'Add to Cart' button is not visible/clickable, try a different item\n"
                f"      - NEVER checkout with less than $15.00 of items unless absolutely no other options exist\n"
                f"      - ALWAYS click 'Proceed to Checkout' and complete the order\n"
                f"      - After checkout, ALWAYS return to the specific date's URL before moving to next date\n"
                f"   f. Only after BOTH lunch and dinner are handled, move to next date\n\n"
                f"Important Notes:\n"
                f"- Stay in the same browser tab throughout\n"
                f"- If login fails, try clicking submit again (note: login flow is buggy and may show incorrect password error even with correct credentials)\n"
                f"- Wait for pages to load after clicking\n"
                f"{dietary_restrictions}\n"
                f"- For each meal (lunch/dinner):\n"
                f"  * First add a healthy main dish (protein-rich meal)\n"
                f"  * Then add healthy sides/extras to maximize the ${self.max_pretax_price} budget\n"
                f"  * ALWAYS complete checkout for each meal separately\n"
                f"  * ALWAYS return to the specific date's URL after checkout\n"
                f"  * ALWAYS verify you're back on the correct date after checkout\n"
                f"- Prioritize this order for item selection:\n"
                f"  1. Protein-rich main dishes (grilled chicken, fish, lean meats)\n"
                f"  2. Salads and grain bowls\n"
                f"  3. Healthy sides (vegetables, fruits)\n"
                f"  4. Additional protein sources\n"
                f"- Report progress after each major step\n"
                f"- If a date is grayed out or not available, skip to the next date\n"
                f"- NEVER move to the next date until both lunch and dinner are handled\n"
            )

            if not self.agent:
                self.agent = Agent(task=task, llm=self.llm)
            else:
                self.agent.task = task

            result = await self.agent.run()
            return True

        except Exception as e:
            logger.error(f"Failed to process all days: {str(e)}")
            return False

    async def close(self):
        """Close browser"""
        # The Agent class handles cleanup automatically 