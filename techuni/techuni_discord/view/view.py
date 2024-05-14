import discord

class ConfirmView(discord.ui.View):
    def __init__(self, timeout: float | None = 180.0):
        super().__init__(timeout=timeout)
        self.value = None

    @discord.ui.button(label="確認", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.send_message("確認しました。", ephemeral=True)
        self.stop()

    @discord.ui.button(label="キャンセル", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.send_message("キャンセルしました。", ephemeral=True)
        self.stop()
