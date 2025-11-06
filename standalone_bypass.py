import asyncio
from playwright.async_api import async_playwright
import json
import os

class NanoLinksBypasser:
    def __init__(self):
        self.first_redirect_url = None
        self.current_progress = 0

    async def update_progress(self, percentage):
        """Print progress"""
        filled = int((percentage / 100) * 20)
        bar = "█" * filled + "░" * (20 - filled)
        print(f"
{bar} {percentage}%", end="", flush=True)

    async def click_button_all_methods(self, page, search_text, button_id=None):
        """Click button using all possible methods"""
        try:
            await page.evaluate("""() => {
                const buttons = document.querySelectorAll("button");
                buttons.forEach(btn => {
                    btn.style.display = "block";
                    btn.style.visibility = "visible";
                    btn.style.pointerEvents = "auto";
                    btn.style.opacity = "1";
                    btn.disabled = false;
                });
            }""")

            if button_id:
                try:
                    element = await page.query_selector(f"#{button_id}")
                    if element:
                        await element.click()
                        return True
                except:
                    pass

            try:
                buttons = await page.query_selector_all("button")
                for btn in buttons:
                    text = await btn.text_content()
                    if text and search_text.upper() in text.upper():
                        await btn.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        await btn.click()
                        await asyncio.sleep(2)
                        return True
            except:
                pass

            try:
                result = await page.evaluate(f"""() => {{
                    const buttons = document.querySelectorAll("button");
                    for (let btn of buttons) {{
                        if (btn.textContent.toUpperCase().includes('{search_text.upper()}')) {{
                            btn.click();
                            return true;
                        }}
                    }}
                    return false;
                }}""")
                if result:
                    await asyncio.sleep(2)
                    return True
            except:
                pass

            return False
        except:
            return False

    async def click_button_javascript_only(self, page, search_text):
        """Click button using JavaScript only"""
        try:
            result = await page.evaluate(f"""() => {{
                const buttons = document.querySelectorAll("button");
                for (let btn of buttons) {{
                    if (btn.textContent.toUpperCase().includes('{search_text.upper()}')) {{
                        btn.click();
                        return true;
                    }}
                }}
                return false;
            }}""")
            if result:
                await asyncio.sleep(2)
                return True
            return False
        except:
            return False

    async def bypass_nanolinks(self, url):
        """Bypass nanolinks URL"""
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                )

                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()

                # STEP 1
                await self.update_progress(11)
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                await asyncio.sleep(2)

                # STEP 2
                await self.update_progress(22)
                try:
                    await page.evaluate("""() => {
                        const popup = document.getElementById('adrinoPop3');
                        if (popup) popup.remove();
                        document.body.style.overflow = 'auto';
                    }""")
                except:
                    pass
                await asyncio.sleep(1)

                # STEP 3
                await self.update_progress(33)
                for i in range(30):
                    if await self.click_button_all_methods(page, "CONTINUE"):
                        break
                    await asyncio.sleep(1)

                # STEP 4
                await self.update_progress(44)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)

                # STEP 5
                await self.update_progress(55)
                await self.click_button_javascript_only(page, "CLICK HERE TO PROCEED")
                await asyncio.sleep(2)

                # STEP 6
                await self.update_progress(66)
                for i in range(30):
                    if await self.click_button_all_methods(page, "CONTINUE"):
                        break
                    await asyncio.sleep(1)

                # STEP 7
                await self.update_progress(77)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1)

                # STEP 8
                await self.update_progress(88)
                last_url = page.url
                self.first_redirect_url = None

                async def on_frame_nav(frame):
                    if frame == page.main_frame:
                        current = page.url
                        if "nanolinks" not in current.lower() and current != last_url:
                            if not self.first_redirect_url:
                                self.first_redirect_url = current

                page.on("framenavigated", on_frame_nav)

                for i in range(10):
                    if await self.click_button_javascript_only(page, "GET LINK"):
                        break
                    await asyncio.sleep(1)

                # STEP 9
                for wait_idx in range(100):
                    if self.first_redirect_url:
                        await self.update_progress(100)
                        print("
✅ Success!")
                        await browser.close()
                        return self.first_redirect_url
                    await asyncio.sleep(0.1)

                await self.update_progress(100)
                print("
✅ Completed")
                final_url = page.url
                await browser.close()
                return final_url

            except Exception as e:
                print(f"
❌ Error: {str(e)}")
                return None

async def main():
    # Your specific link
    test_url = "https://nanolinks.in/PY1g"
    
    print(f"🔄 Bypassing: {test_url}
")
    
    bypasser = NanoLinksBypasser()
    result = await bypasser.bypass_nanolinks(test_url)
    
    if result:
        print(f"
🔗 Final URL: {result}")
        
        # Save result to file
        with open("bypass_results.json", "w") as f:
            json.dump({
                "source_url": test_url,
                "final_url": result, 
                "success": True
            }, f, indent=2)
        print("✅ Result saved to bypass_results.json")
    else:
        with open("bypass_results.json", "w") as f:
            json.dump({
                "source_url": test_url,
                "success": False
            }, f, indent=2)
        print("❌ Failed to bypass")

if __name__ == "__main__":
    asyncio.run(main())
