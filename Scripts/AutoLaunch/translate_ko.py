import asyncio

import iterm2
from googletrans import Translator


def to_html(text):
    return "<pre>" + text.replace("&", "&amp;").replace("<", "&lt;") + "</pre>"


async def translate(text):
    await asyncio.sleep(0)
    translator = Translator()
    return translator.translate(text, dest='ko').text


async def main(connection):
    app = await iterm2.async_get_app(connection)

    # Set the click handler
    @iterm2.RPC
    async def onclick(session_id):
        session = app.get_session_by_id(session_id)
        selection = await session.async_get_selection()
        selected_text = await session.async_get_selection_text(selection)
        translated_text = await translate(selected_text)
        await component.async_open_popover(session_id, to_html(translated_text), iterm2.util.Size(600, 600))

    # Define the configuration knobs:
    vl = "translation_ko"
    knobs = [iterm2.CheckboxKnob("Translation Ko", False, vl)]
    component = iterm2.StatusBarComponent(
        short_description="Translation Ko",
        detailed_description="Select text in the terminal, then click this status bar component to see it translated.",
        knobs=knobs,
        exemplar="Translate Ko",
        update_cadence=None,
        identifier="com.iterm2.translation-ko")

    # This function gets called whenever any of the paths named in defaults (below) changes
    # or its configuration changes.
    @iterm2.StatusBarRPC
    async def coro(knobs):
        return ["Translate Ko"]

    # Register the component.
    await component.async_register(connection, coro, onclick=onclick)


iterm2.run_forever(main)
