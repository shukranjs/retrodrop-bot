from typing import Optional

from telegram import Update, User
from telegram.ext import ContextTypes


async def get_user_id_from_channel(
    update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: str
) -> Optional[int]:
    """
    Retrieves the user ID from a message in a Telegram channel or chat.

    This function checks the `from_user` attribute in the incoming `Update`.
    If the `from_user` is available (i.e., the message is not anonymous),
    it returns the user ID. Otherwise, it sends a message to the provided
    chat ID informing that the user cannot be identified.

    Args:
        update (Update): The Telegram update object containing the message details.
        context (ContextTypes.DEFAULT_TYPE): The context provided by the `telegram.ext` for bot interaction.
        chat_id (str): The chat ID where the bot will send a message if the user cannot be identified.

    Returns:
        Optional[int]: The user ID of the message sender, or `None` if the user is not identifiable.
    """
    from_user: Optional[User] = update.effective_message.from_user
    if from_user is None:
        # Notify in the chat that the user could not be identified
        await context.bot.send_message(
            chat_id=chat_id,
            text="Unable to identify the user who sent this message.",
        )
        return None

    # Return the ID of the identified user
    return from_user.id
