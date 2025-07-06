import discord
from discord.ext import commands
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import pytz
import io

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_USER_ID = 123456789012345678  # Replace with actual user ID
BD_TIMEZONE = pytz.timezone('Asia/Dhaka')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    if any(word in content for word in ['purge', 'purging', 'purged', 'purg', 'parge', 'parg', 'parging']):
        messages = [msg async for msg in message.channel.history(limit=100, before=message.created_at)]
        if not messages:
            return

        messages.sort(key=lambda x: x.created_at)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph(f"Messages from {message.channel.name}", styles['Title']), Spacer(1, 12)]

        for msg in messages:
            ts = msg.created_at.astimezone(BD_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
            story.append(Paragraph(f"[{ts}] {msg.author.name}: {msg.content}", styles['Normal']))
            story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)

        user = await bot.fetch_user(TARGET_USER_ID)
        if user:
            now = datetime.now(BD_TIMEZONE).strftime('%Y%m%d_%H%M%S')
            await user.send(
                f"Messages from {message.channel.name} before they got purged:",
                file=discord.File(buffer, filename=f"purged_messages_{now}.pdf")
            )

        buffer.close()

    await bot.process_commands(message)

bot.run('YOUR_BOT_TOKEN')
