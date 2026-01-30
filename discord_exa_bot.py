#!/usr/bin/env python3
"""
Discord Self-Bot with Exa Integration
Responds with Exa answers when someone @mentions exa
"""

import discord
import os
import re
import sys
from dotenv import load_dotenv
import requests

# Force unbuffered output
sys.stdout = sys.__stdout__
os.environ['PYTHONUNBUFFERED'] = '1'

def log(msg):
    print(msg, flush=True)

load_dotenv()  # Load from .env if present, otherwise use system env vars

DISCORD_USER_TOKEN = os.getenv('DISCORD_USER_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', 0))
EXA_API_KEY = os.getenv('EXA_API_KEY')


class ExaBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.target_channel = None
        self.last_links = None  # Store links from last Exa response

    async def on_ready(self):
        log(f'✓ Logged in as {self.user.name}')
        self.target_channel = self.get_channel(CHANNEL_ID)

        if self.target_channel:
            log(f'✓ Monitoring DM group for @exa mentions')
            log(f'✓ Bot is ready!\n')
        else:
            log(f'✗ Could not find channel {CHANNEL_ID}')

    async def on_message(self, message):
        # Debug: print all messages
        log(f"[DEBUG] Message in channel {message.channel.id} from {message.author.name}: {message.content[:50]}")

        # Only from target channel
        if message.channel.id != CHANNEL_ID:
            log(f"[DEBUG] Wrong channel: {message.channel.id} != {CHANNEL_ID}")
            return

        # Check for /links command
        if message.content.strip().lower() == '/links':
            if self.last_links:
                log(f"📎 Sending stored links")
                await message.channel.send(self.last_links)
            else:
                await message.channel.send("No links stored yet")
            return

        # Check if message mentions @exa
        if '@exa' in message.content.lower():
            log(f"\n📨 {message.author.name}: {message.content}")

            # Extract the question (everything after @exa)
            question = re.sub(r'@exa\s*', '', message.content, flags=re.IGNORECASE).strip()

            if not question:
                await message.channel.send("Ask me something after @exa!")
                return

            log(f"🔍 Searching Exa for: {question}")

            # Call Exa API
            answer, links = await self.get_exa_answer(question)

            if answer:
                self.last_links = links  # Store links for /links command
                log(f"✓ Sending answer ({len(answer)} chars)")
                await message.channel.send(answer)
            else:
                log(f"✗ No answer from Exa")
                await message.channel.send("Couldn't find an answer, sorry!")

    async def get_exa_answer(self, question):
        """Call Exa's answer API. Returns (answer, links) tuple."""

        if not EXA_API_KEY:
            return ("❌ Exa API key not set! Add it to .env file", None)

        try:
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': EXA_API_KEY
            }

            payload = {
                'query': question
            }

            # Call Exa answer API
            response = requests.post(
                'https://api.exa.ai/answer',
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                answer_text = data.get('answer', '')
                citations = data.get('citations', [])

                if answer_text:
                    # Format links from citations
                    links = None
                    if citations:
                        links = "**Sources:**\n"
                        for i, cite in enumerate(citations[:5], 1):
                            url = cite.get('url', '')
                            title = cite.get('title', 'Source')
                            if url:
                                links += f"{i}. {title}\n   {url}\n"

                    return (answer_text, links)
                else:
                    return ("No answer found", None)
            else:
                log(f"Exa API error: {response.status_code} - {response.text}")
                return (f"Exa API error: {response.status_code}", None)

        except Exception as e:
            log(f"Error calling Exa: {e}")
            return (f"Error: {e}", None)


def main():
    log("="*70)
    log("Discord Exa Bot")
    log("Responds when someone mentions @exa")
    log("="*70)
    log("")

    if not DISCORD_USER_TOKEN:
        log("⚠️  Missing DISCORD_USER_TOKEN in .env")
        return

    if not EXA_API_KEY:
        log("⚠️  Missing EXA_API_KEY - get one from https://exa.ai")
        log("    Then add to .env: EXA_API_KEY=your-key-here")
        log("")

    client = ExaBot()

    try:
        client.run(DISCORD_USER_TOKEN)
    except KeyboardInterrupt:
        log("\n\n✓ Stopped")
    except Exception as e:
        log(f"\n✗ Error: {e}")


if __name__ == '__main__':
    main()
