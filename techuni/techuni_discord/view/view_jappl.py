import discord
from .view import ConfirmView
from techuni.techuni_object import JoinApplicationStatus

class JoinApplicationDecideView(discord.ui.View):
    FORUM_CHANNEL: discord.ForumChannel = None
    CONFIRM_TIMEOUT = 60
    INVITE_FUNCTION = None
    DATABASE_SESSION = None

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="受理する", style=discord.ButtonStyle.green, custom_id="jappl_decide:accept")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        is_valid, thread, forum_channel = await _interaction_check(interaction)
        if not is_valid:
            await interaction.response.send_message("この申請は審査中ではありません。", ephemeral=True, delete_after=30)
            return

        if await self._run(interaction, True):
            self.stop()

    @discord.ui.button(label="却下する", style=discord.ButtonStyle.red, custom_id="jappl_decide:reject")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        is_valid, thread, forum_channel = await _interaction_check(interaction)
        if not is_valid:
            await interaction.response.send_message("この申請は審査中ではありません。", ephemeral=True, delete_after=30)
            return

        if await self._run(interaction, False):
            self.stop()

    async def _run(self, interaction: discord.Interaction, value: bool) -> bool:
        confirm_view = ConfirmView(timeout=self.CONFIRM_TIMEOUT)
        await interaction.response.send_message(
            "この入会申請を{0}しますか？".format("受理" if value else "却下"),
            view=confirm_view,
            ephemeral=True,
            delete_after=self.CONFIRM_TIMEOUT
        )
        await confirm_view.wait()

        interaction_stop = False
        if confirm_view.value is not None:  # -> if not timeout
            if confirm_view.value:
                interaction_stop = await set_application_status(interaction, value)
        return interaction_stop

async def set_application_status(interaction: discord.Interaction, status: bool) -> bool:
    # response is already used
    is_valid, thread, forum_channel = await _interaction_check(interaction)
    if not is_valid:
        await interaction.followup.send("この申請は審査中ではありません。", ephemeral=True, timeout=30)
        return False

    if status:
        new_tag_info = [JoinApplicationStatus.INVITE.get_tag(forum_channel)], "[フラグ設定] 入会申請の受理"
        await thread.send(
            "この入会申請は受理されました。(実行者：{0})".format(interaction.user.mention),
            allowed_mentions=discord.AllowedMentions(users=True)
        )
        link: discord.Invite = await JoinApplicationDecideView.INVITE_FUNCTION(thread.name)
        await thread.send(
            "招待リンク： ||{0}||".format(link.url),  # markdownのスポイラー(||)で目隠しして送信
            suppress_embeds=True  # 招待リンクの埋め込みを表示しない
        )

    else:
        new_tag_info = [JoinApplicationStatus.REJECT.get_tag(forum_channel)], "[フラグ設定] 入会申請の却下"
        await thread.send(
            "この入会申請は却下されました。(実行者：{0})".format(interaction.user.mention),
            allowed_mentions=discord.AllowedMentions(users=True)
        )

    # タグ設定
    await thread.edit(applied_tags=new_tag_info[0], reason=new_tag_info[1])

    # 受理・却下ボタン(View)削除
    try:
        first_message = await thread.fetch_message(thread.id)  # is not None (ないときはNotFound例外)
        await first_message.edit(view=None)
    except discord.NotFound:
        pass

    # スレッドのロック・クローズ処理
    await thread.edit(archived=True, locked=True)

    JoinApplicationDecideView.DATABASE_SESSION.delete_application_by_thread(thread.id)

    return True

async def _interaction_check(interaction: discord.Interaction) -> tuple[bool, discord.Thread | None, discord.ForumChannel | None]:
    thread = interaction.channel
    if not isinstance(thread, discord.Thread):
        raise ValueError(f"deciding channel is not in Thread but {type(thread)}")

    forum_channel = thread.parent
    if not isinstance(forum_channel, discord.ForumChannel):
        raise ValueError(f"thread parent is not ForumChannel but {type(forum_channel)}")

    if forum_channel.id != JoinApplicationDecideView.FORUM_CHANNEL.id:
        raise ValueError(f"thread parent is not Join Application Channel: {forum_channel.name}(id: {forum_channel.id})")

    receive_tag = JoinApplicationStatus.RECEIVE.get_tag(forum_channel)
    if receive_tag not in thread.applied_tags:
        return False, None, None

    return True, thread, forum_channel
