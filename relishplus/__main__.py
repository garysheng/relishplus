"""
Main entry point for RelishPlus automation
"""
import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler
from .automation import RelishAutomation
from .config import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger(__name__)

def get_credentials() -> tuple[str, str]:
    """Get credentials from environment variables"""
    email = os.getenv("RELISH_EMAIL")
    password = os.getenv("RELISH_PASSWORD")
    
    if not email or not password:
        logger.error(
            "Missing credentials. Please set RELISH_EMAIL and RELISH_PASSWORD environment variables"
        )
        raise typer.Exit(1)
        
    return email, password

async def run_automation():
    """Run the RelishPlus automation"""
    try:
        # Load config and get credentials
        config = load_config()
        email, password = get_credentials()
        
        # Initialize automation
        automation = RelishAutomation(email, password, config)
        
        # Create progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            # Add progress display
            progress.add_task(description="Ordering meals...", total=None)
            
            # Run the automation
            if not await automation.order_all_days():
                logger.error("Automation failed")
                return False
                
            logger.info("Automation completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"Automation failed: {str(e)}")
        return False
        
    finally:
        if "automation" in locals():
            await automation.close()

def main():
    """Main entry point"""
    try:
        asyncio.run(run_automation())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    main() 