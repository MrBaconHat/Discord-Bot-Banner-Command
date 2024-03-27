import discord
from discord.ext import commands
import requests


token = 'paste your bot token here....'


def get_user_banner(user_id):

    url = f'https://discord.com/api/v10/users/{user_id}'

    headers = {
            'Authorization': f"Bot {token}"
    }

    response = requests.get(url=url, headers=headers)
    json_data = response.json()

    if response.status_code == 200:
        user_banner = json_data['banner']
        return user_banner

    elif response.status_code == 404 and response.reason == 'Not Found':
        message = json_data['message']
        return message


def banner_link_check(user_id, banner_url):
    banner_types = ['.png?size=512', '.gif?size=512', '.jpg?size=512', 'jpeg?size=512']

    for types in banner_types:

        banner_link_checking = f'https://cdn.discordapp.com/banners/{user_id}/{banner_url}{types}'
        response = requests.get(banner_link_checking)

        if response.status_code == 200:
            return banner_link_checking
    return None



@bot.hybrid_command(name='banner', description='Returns users banner')
async def banner(ctx, user: discord.User = None):

    user_id = user.id if user else ctx.author.id

    returned_response = get_user_banner(user_id=user_id)

    if returned_response:
        banner_link_validation_check_response = banner_link_check(user_id, returned_response)

        if banner_link_validation_check_response:
            await ctx.send(content=banner_link_validation_check_response)
        else:
            await ctx.send('there was an unexpected error...')

    elif not returned_response:
        await ctx.send(f'**{user.name}** have no banner...')



@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Successfully logged in as: {bot.user.name}')


bot.run(token)
