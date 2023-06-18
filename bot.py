import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler
from imdb import IMDb

# Initialize the IMDbPY library
ia = IMDb()

# Telegram bot token obtained from BotFather
TOKEN = "6175592645:AAGFojrbkUA7Us58E2wexSjL-W5bpSNvr-c"

def start(update, context):
    """Handler function for the /start command."""
    keyboard = [
        [InlineKeyboardButton("Developer", url="https://harshitethic.in")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_path = "imdb.png"

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'),
                           caption="Welcome to IMDb Bot!\nFor Help Menu Type: /help\nClick the button below to learn more about the developer.",
                           reply_markup=reply_markup)


def help_command(update, context):
    """Handler function for the /help command."""
    help_text = "This is a bot that provides details about movies.\n\n" \
                "Usage:\n" \
                "/movie [title] - Get details and images of a movie.\n\n" \
                "Example:\n" \
                "/movie The Shawshank Redemption"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def movie_command(update, context):
    """Handler function for the /movie command."""
    args = context.args
    if not args:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a movie title.")
        return

    title = ' '.join(args)
    movies = ia.search_movie(title)
    if not movies:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No movie found with that title.")
        return

    movie = movies[0]
    ia.update(movie)

    movie_details = f"<b>Title:</b> {movie.get('title')} ({movie.get('year')})\n"
    movie_details += f"<b>Rating:</b> {movie.get('rating')}\n"
    movie_details += f"<b>Genres:</b> {', '.join(movie.get('genres', []))}\n"
    movie_details += f"<b>Plot:</b> {movie.get('plot')[0]}\n"

    # Send movie poster image, if available
    if movie.get('cover url'):
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=movie.get('cover url'), caption=movie_details, parse_mode=telegram.ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=movie_details, parse_mode=telegram.ParseMode.HTML)


def main():
    """Main function to start the bot."""
    # Create an instance of the Telegram Updater
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("movie", movie_command))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
