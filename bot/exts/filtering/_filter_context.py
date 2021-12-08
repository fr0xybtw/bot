from discord import Embed, Message, TextChannel, User

from dataclasses import dataclass, field


@dataclass
class FilterContext:
    # Input context
    event: str
    author: User
    message: Message
    channel: TextChannel
    content: str
    embeds: list = field(default_factory=list)
    # Output context
    dm_text: str = field(default_factory=str)
    dm_embed: Embed = field(default_factory=Embed)
    send_alert: bool = field(default=True)
    alert_content: str = field(default_factory=str)
    alert_embeds: list = field(default_factory=list)
