import asyncio
from corefoundationasyncio import CoreFoundationEventLoop

# Make sure these classes are loaded
from fontgoggles.mac.document import FGDocument  # noqa: F401
from fontgoggles.mac.appDelegate import FGAppDelegate  # noqa: F401


if __name__ == "__main__":
    loop = CoreFoundationEventLoop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        loop.close()
