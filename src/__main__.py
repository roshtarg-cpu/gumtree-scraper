"""Package entry point for running as module."""
import asyncio
from .main import main

if __name__ == '__main__':
    asyncio.run(main())
